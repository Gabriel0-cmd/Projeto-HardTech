"""Módulo de web scrapers para lojas de hardware."""

from .base_scraper import BaseScraper
from .kabum_scraper import KabumScraper
from .terabyte_scraper import TerabyteScraper
from .pichau_scraper import PichauScraper
from .amazon_scraper import AmazonBrasilScraper
from .mercadolivre_scraper import MercadoLivreScraper
from .newegg_scraper import NeweggBrasilScraper

__all__ = [
    "BaseScraper",
    "KabumScraper",
    "TerabyteScraper",
    "PichauScraper",
    "AmazonBrasilScraper",
    "MercadoLivreScraper",
    "NeweggBrasilScraper",
]
