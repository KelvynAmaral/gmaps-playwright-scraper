<div align="center">

# 🗺️ GMaps Playwright Scraper
### Inteligência de Mercado & Extração de Dados Locais

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Automated-green?style=for-the-badge&logo=playwright)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<p align="center">
  Uma ferramenta robusta de <b>Web Scraping</b> focada na extração de leads qualificados do Google Maps.<br>
  Projetada para superar bloqueios, carregar listas infinitas e extrair dados visuais com precisão.
</p>

</div>

---

## 📋 Sobre o Projeto

Este projeto é um extrator de dados de alta performance desenvolvido para mapear estabelecimentos comerciais. Diferente de scrapers tradicionais baseados em requisições HTTP (que são facilmente bloqueados), este projeto utiliza o **Playwright** para simular um navegador real (Chromium).

Atualmente, o projeto está configurado para uma varredura granular (nível de bairro) na cidade de **Belo Horizonte/MG**, focada no mercado de **Beleza e Estética**.

### 🚀 Diferenciais Técnicos

* **🔍 Navegação Direta:** Constrói URLs de busca dinâmicas para evitar a interação com a barra de pesquisa, reduzindo drasticamente a detecção de bots.
* **👁️ Extração Visual (Visual Regex):** Ignora metadados ocultos (que o Google altera frequentemente) e captura a nota e quantidade de avaliações lendo o texto renderizado na tela (ex: `4,8 (1.205)`).
* **🛡️ Evasão de Bloqueios:** Utiliza User-Agent de navegador real (Chrome/Windows), delays aleatórios e scrolls humanizados.
* **💾 Persistência Incremental:** Salva arquivos parciais (`.csv`) a cada bairro finalizado. Se o script for interrompido, os dados coletados até o momento estão seguros.
* **🧩 Consolidação Inteligente:** Inclui um script dedicado para unificar os arquivos parciais e remover duplicatas (Deduplicação por `Nome + Endereço`).

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função |
| :--- | :--- |
| **Python 3.9+** | Linguagem base. |
| **Playwright** | Automação de navegador e renderização de JS. |
| **Pandas** | Manipulação de DataFrames, limpeza e exportação (CSV/Excel). |
| **Regex** | Extração de padrões textuais complexos. |

---

## 📦 Instalação e Configuração

Siga os passos abaixo para preparar o ambiente de desenvolvimento.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/gmaps-playwright-scraper.git](https://github.com/seu-usuario/gmaps-playwright-scraper.git)
cd gmaps-playwright-scraper