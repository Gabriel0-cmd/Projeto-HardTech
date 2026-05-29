"""Classe base para scrapers de lojas de hardware."""

import time
from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup
from src.config import SCRAPER_CONFIG
from src.models import Product
from src.utils import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """Classe base para implementar scrapers de lojas."""

    def __init__(self, store_name: str, base_url: str):
        """
        Inicializa o scraper.

        Args:
            store_name: Nome da loja (ex: 'Kabum')
            base_url: URL base da loja
        """
        self.store_name = store_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": SCRAPER_CONFIG["user_agent"]
        })
        self.timeout = SCRAPER_CONFIG["timeout"]
        self.retries = SCRAPER_CONFIG["retries"]
        self.delay = SCRAPER_CONFIG["delay"]

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Faz o download e parse de uma página.

        Args:
            url: URL da página a baixar

        Returns:
            BeautifulSoup object ou None se falhar
        """
        for attempt in range(self.retries):
            try:
                logger.info(f"[{self.store_name}] Baixando {url}")
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    verify=True
                )
                response.raise_for_status()

                time.sleep(self.delay)  # Respeitar o servidor
                return BeautifulSoup(response.content, "html.parser")

            except requests.exceptions.Timeout:
                logger.warning(
                    f"[{self.store_name}] Timeout na tentativa {attempt + 1}/{self.retries}"
                )
            except requests.exceptions.RequestException as e:
                logger.error(
                    f"[{self.store_name}] Erro ao baixar {url}: {e}"
                )

            # Aguardar antes de retornar
            if attempt < self.retries - 1:
                time.sleep(2 ** attempt)  # Backoff exponencial

        logger.error(f"[{self.store_name}] Falha ao baixar {url} após {self.retries} tentativas")
        return None

    @abstractmethod
    def search_products(self, query: str, category: str = None) -> list[Product]:
        """
        Busca produtos pela query.

        Args:
            query: Termo de busca (ex: 'Processador Intel i5')
            category: Categoria do produto (opcional)

        Returns:
            Lista de produtos encontrados
        """
        pass

    @abstractmethod
    def get_product_details(self, product_url: str) -> Optional[Product]:
        """
        Obtém detalhes de um produto específico.

        Args:
            product_url: URL do produto

        Returns:
            Objeto Product com detalhes ou None
        """
        pass

    def close(self):
        """Fecha a sessão do scraper."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
