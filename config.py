import logging

# Configurações de Log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger("BeautyScraper")

# Configurações de Scraping
HEADLESS = False  
TIMEOUT = 30000   
MAX_RESULTS_PER_CITY = 20  # Garante busca de até 20 itens por bairro

# Termos de Busca
TERMOS = [
    "Salão de Beleza",
    "Cabeleireiro",
    "Hair Designer",
    "Manicure",
    "Esmalteria",
    "Nail Designer",
    "Designer de Unhas",
    "Designer de Sobrancelha",
    #"Esteticista",
    #"Clínica de Estética",
    #"Centro de Estética",
    #"Estética Facial",
    #"Estética Corporal",
    #"Spa",
    "Depilação",
    "Micropigmentação"
]

# Lista de Bairros de Belo Horizonte
BAIRROS_BH = [
    # Região Centro-Sul
    "Savassi", "Funcionários", "Lourdes", "Centro", "Santo Agostinho", 
    "Serra", "Sion", "Anchieta", "São Pedro", "Carmo", "Cruzeiro", 
    "Mangabeiras", "Belvedere", "Santa Efigênia", "Santa Lúcia",

    # Região Oeste
    #"Buritis", "Estoril", "Palmeiras", "Nova Suíça", "Grajaú", 
    #"Gutierrez", "Prado", "Barroca", "Calafate", "Nova Granada", "Havaí",

    # Região Pampulha
    #"Pampulha", "Ouro Preto", "Itapoã", "Santa Amélia", "Castelo", 
    #"Paquetá", "Santa Branca", "São Luiz",

    # Região Nordeste
    #"União", "Cidade Nova", "Silveira", "Ipiranga", "Nova Floresta", 
    #"Cachoeirinha", "São Gabriel", "Guarani",

    # Região Norte
    #"Planalto", "Heliópolis", "Jaqueline", "Juliana", "Ribeiro de Abreu",

    # Região Noroeste
    #"Caiçaras", "Padre Eustáquio", "Dom Cabral", "Carlos Prates", "Alto dos Pinheiros",

    # Região Leste
    #"Floresta", "Santa Tereza", "Horto", "Sagrada Família", "Colégio Batista",

    # Região Barreiro
    #"Barreiro", "Diamante", "Milionários", "Águas Claras", "Cardoso"
]