import re
import random
import time
import urllib.parse
from playwright.sync_api import sync_playwright, Page, Locator
from typing import List, Optional
from config import LOGGER, HEADLESS, TIMEOUT, MAX_RESULTS_PER_CITY
from models.establishment import Establishment

class GoogleMapsScraper:
    def __init__(self):
        pass
        
    def _random_sleep(self, min_s: float = 1.0, max_s: float = 3.0):
        time.sleep(random.uniform(min_s, max_s))

    def _handle_consent(self, page: Page):
        """Tenta fechar modais de cookies/consentimento."""
        try:
            selectors = [
                "button[aria-label='Aceitar tudo']",
                "button:has-text('Aceitar tudo')",
                "form[action*='consent'] button",
                "button:has-text('Concordo')"
            ]
            for sel in selectors:
                if page.locator(sel).is_visible(timeout=2000):
                    page.click(sel)
                    self._random_sleep()
                    break
        except:
            pass

    def _parse_address(self, full_address: str) -> dict:
        parts = {"rua": None, "bairro": None, "cidade": None, "estado": None, "cep": None}
        if not full_address: return parts
        tokens = [t.strip() for t in re.split(r'[,\-]', full_address)]
        if len(tokens) >= 4:
            parts["cep"] = tokens[-1] if re.match(r'\d{5}', tokens[-1]) else None
            parts["estado"] = tokens[-2] if len(tokens[-2]) == 2 else None
            parts["cidade"] = tokens[-3]
            parts["bairro"] = tokens[-4]
            parts["rua"] = full_address.split("-")[0].strip()
        return parts

    def _extract_coordinates(self, url: str) -> tuple[Optional[float], Optional[float]]:
        try:
            lat = re.search(r'!3d([-0-9.]+)', url)
            lon = re.search(r'!4d([-0-9.]+)', url)
            return (float(lat.group(1)) if lat else None, float(lon.group(1)) if lon else None)
        except:
            return None, None

    def _scroll_feed(self, page: Page):
        try:
            # Tenta localizar o feed de resultados
            feed = page.locator("div[role='feed']")
            if not feed.count():
                feed = page.locator("div.m6QErb[aria-label^='Resultados de']")
            
            if not feed.count():
                LOGGER.warning("Feed de rolagem não encontrado.")
                return

            LOGGER.info("Rolando lista para carregar mais itens...")
            # Scroll ajustado para garantir o carregamento até o limite configurado
            # O Max garante pelo menos 3 scrolls
            num_scrolls = max(3, MAX_RESULTS_PER_CITY // 4)
            
            for _ in range(num_scrolls):
                feed.first.evaluate("element => element.scrollTop = element.scrollHeight")
                self._random_sleep(1.5, 3)
                if page.locator("text=Você chegou ao final da lista").is_visible():
                    break
        except Exception as e:
            LOGGER.warning(f"Aviso no scroll: {e}")

    def scrape_city(self, termo: str, localizacao: str) -> List[Establishment]:
        results = []
        
        with sync_playwright() as p:
            # Configuração do navegador
            browser = p.chromium.launch(headless=HEADLESS, args=["--start-maximized"])
            context = browser.new_context(
                viewport={"width": 1366, "height": 768},
                locale="pt-BR",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # Navegação Direta
                query = urllib.parse.quote_plus(f"{termo} em {localizacao}")
                url_direta = f"https://www.google.com.br/maps/search/{query}?hl=pt-BR"
                
                LOGGER.info(f"Navegando para: {localizacao} | URL: {url_direta}")
                page.goto(url_direta, timeout=TIMEOUT)
                
                self._handle_consent(page)

                # Verifica carregamento
                try:
                    page.wait_for_selector("a.hfpxzc", timeout=15000)
                except:
                    LOGGER.error(f"Sem resultados visíveis para {localizacao}.")
                    return []

                self._scroll_feed(page)
                
                listings = page.locator("a.hfpxzc").all()
                LOGGER.info(f"Encontrados {len(listings)} locais em {localizacao}.")
                
                processed_urls = set()

                for idx, listing in enumerate(listings[:MAX_RESULTS_PER_CITY]):
                    try:
                        href = listing.get_attribute("href")
                        if not href or href in processed_urls: continue
                        processed_urls.add(href)

                        # Clica e aguarda
                        listing.click()
                        self._random_sleep(1, 2)
                        
                        try:
                            page.wait_for_selector("h1.DUwDvf", timeout=5000)
                        except:
                            continue

                        # --- Extração de Dados ---
                        nome = page.locator("h1.DUwDvf").first.inner_text()
                        
                        # --- ESTRATÉGIA VISUAL (Regex) para Nota e Reviews ---
                        rating_val = 0.0
                        reviews_val = 0
                        
                        try:
                            # O Google agrupa Nota e Avaliações na div com classe 'F7nice'
                            # Exemplo de texto capturado: "4,8(1.205)" ou "5,0\n(15)"
                            rating_container = page.locator("div.F7nice").first
                            
                            if rating_container.count():
                                raw_text = rating_container.inner_text()
                                
                                # 1. Extrair Nota (procura padrão n,n ou n.n)
                                # Ex: Pega "4,8" de "4,8(150)"
                                rating_match = re.search(r'(\d+[\.,]\d+)', raw_text)
                                if rating_match:
                                    rating_val = float(rating_match.group(1).replace(',', '.'))
                                
                                # 2. Extrair Quantidade (procura números dentro de parênteses)
                                # Ex: Pega "1.205" de "(1.205)"
                                reviews_match = re.search(r'\(([\d\.]+)\)', raw_text)
                                if reviews_match:
                                    # Remove pontos de milhar (1.205 -> 1205) e converte
                                    clean_num = reviews_match.group(1).replace('.', '')
                                    reviews_val = int(clean_num)
                                    
                        except Exception as e:
                            LOGGER.warning(f"Erro ao parsear nota/reviews visualmente: {e}")

                        # --- Outros Campos ---
                        cat_el = page.locator("button[jsaction*='category']").first
                        categoria = cat_el.inner_text() if cat_el.count() else None

                        btn_addr = page.locator("button[data-item-id='address']")
                        endereco = btn_addr.get_attribute("aria-label").replace("Endereço: ", "") if btn_addr.count() else None
                        
                        btn_phone = page.locator("button[data-item-id*='phone']")
                        telefone = btn_phone.get_attribute("aria-label").replace("Telefone: ", "") if btn_phone.count() else None

                        lat, lon = self._extract_coordinates(page.url)
                        addr_parts = self._parse_address(endereco)

                        est = Establishment(
                            nome=nome, 
                            rating=rating_val, 
                            reviews_count=reviews_val, 
                            categoria=categoria,
                            telefone=telefone, 
                            endereco_completo=endereco,
                            rua=addr_parts["rua"], 
                            bairro=addr_parts["bairro"],
                            cidade=addr_parts["cidade"], 
                            estado=addr_parts["estado"],
                            cep=addr_parts["cep"], 
                            latitude=lat, 
                            longitude=lon, 
                            link=page.url
                        )
                        results.append(est)
                        LOGGER.info(f"Extraído: {est.nome} | Nota: {est.rating} | Reviews: {est.reviews_count}")

                    except Exception as e:
                        LOGGER.error(f"Erro item {idx}: {e}")
                        
            except Exception as e:
                LOGGER.critical(f"Erro local {localizacao}: {e}")
            finally:
                browser.close()
                
        return results