"""Configurações globais do HardTech."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Configurações de Web Scraping
SCRAPER_CONFIG = {
    "timeout": int(os.getenv("SCRAPER_TIMEOUT", 10)),
    "retries": int(os.getenv("SCRAPER_RETRIES", 3)),
    "delay": float(os.getenv("SCRAPER_DELAY", 1.0)),  # Delay entre requisições em segundos
    "user_agent": os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ),
}

# Lojas disponíveis
STORES = {
    "kabum": {
        "name": "Kabum",
        "url": "https://www.kabum.com.br",
        "enabled": True,
    },
    "terabyte": {
        "name": "Terabyte",
        "url": "https://www.terabyteshop.com.br",
        "enabled": True,
    },
    "pichau": {
        "name": "Pichau",
        "url": "https://www.pichau.com.br",
        "enabled": True,
    },
}

# Categorias de produtos
PRODUCT_CATEGORIES = {
    "processador": "Processadores",
    "placa_mae": "Placas-Mãe",
    "memoria_ram": "Memória RAM",
    "ssd": "SSD",
    "hd": "HD",
    "gpu": "Placas de Vídeo",
    "fonte": "Fontes",
    "cooler": "Coolers",
    "gabinete": "Gabinetes",
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# Banco de dados (será implementado depois)
DATABASE_CONFIG = {
    "type": os.getenv("DB_TYPE", "sqlite"),
    "path": DATA_DIR / "hardtech.db",
}
