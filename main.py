from config import BAIRROS_BH, TERMOS, LOGGER
from services.scraper_service import GoogleMapsScraper
from services.export_service import ExportService
from datetime import datetime

def main():
    start_time = datetime.now()
    LOGGER.info("Iniciando processo de scraping focado em BH por bairros...")
    
    scraper = GoogleMapsScraper()
    all_data = []

    for bairro in BAIRROS_BH:
        # Define localização estrita para BH
        localizacao_busca = f"{bairro}, Belo Horizonte, MG"
        
        for termo in TERMOS:
            LOGGER.info(f"--- Iniciando: {termo} em {localizacao_busca} ---")
            
            results = scraper.scrape_city(termo, localizacao_busca)
            
            if results:
                # Salvamento Parcial
                safe_bairro = bairro.replace(" ", "_")
                safe_termo = termo.replace(" ", "_")
                timestamp = datetime.now().strftime('%H%M')
                
                ExportService.export_data(
                    results, 
                    filename_prefix=f"BH_{safe_bairro}_{safe_termo}_{timestamp}"
                )
                
                all_data.extend(results)
            else:
                LOGGER.warning(f"Nenhum resultado para {termo} em {localizacao_busca}")

    LOGGER.info("Gerando arquivo final consolidado...")
    unique_data = { (d.nome, d.endereco_completo): d for d in all_data }.values()
    
    if unique_data:
        ExportService.export_data(
            list(unique_data), 
            filename_prefix=f"LEADS_BH_COMPLETO_{start_time.strftime('%Y%m%d_%H%M')}"
        )
    
    end_time = datetime.now()
    LOGGER.info(f"Processo finalizado em {end_time - start_time}")

if __name__ == "__main__":
    main()