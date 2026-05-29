"""Scraper para a loja Kabum."""

import re
from typing import Optional

from src.models import Product, ProductPrice
from src.utils import setup_logger
from .base_scraper import BaseScraper

logger = setup_logger(__name__)


class KabumScraper(BaseScraper):
    """Scraper para produtos da Kabum."""

    def __init__(self):
        """Inicializa o scraper da Kabum."""
        super().__init__(
            store_name="Kabum",
            base_url="https://www.kabum.com.br"
        )

    def search_products(self, query: str, category: str = None) -> list[Product]:
        """
        Busca produtos na Kabum.

        Args:
            query: Termo de busca
            category: Categoria (opcional)

        Returns:
            Lista de produtos encontrados
        """
        products = []

        try:
            # URL de busca da Kabum
            search_url = f"{self.base_url}/busca/{query}"
            logger.info(f"Buscando '{query}' na Kabum...")

            soup = self.fetch_page(search_url)
            if not soup:
                logger.error("Não consegui baixar a página de busca")
                return products

            # Procurar pelos produtos (você pode precisar ajustar o seletor)
            # Exemplo: div class="product" ou similar
            product_elements = soup.find_all("div", class_="product-item")

            logger.info(f"Encontrados {len(product_elements)} produtos")

            for element in product_elements[:10]:  # Limitar a 10 produtos
                try:
                    product = self._parse_product_element(element)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.warning(f"Erro ao parsear produto: {e}")
                    continue

        except Exception as e:
            logger.error(f"Erro durante busca: {e}")

        return products

    def _parse_product_element(self, element) -> Optional[Product]:
        """
        Extrai informações de um elemento de produto.

        Args:
            element: Elemento BeautifulSoup do produto

        Returns:
            Objeto Product ou None
        """
        try:
            # Extrair título
            title_elem = element.find("h2", class_="product-title")
            if not title_elem:
                return None

            title = title_elem.text.strip()

            # Extrair preço
            price_elem = element.find("span", class_="product-price")
            if not price_elem:
                return None

            price_text = price_elem.text.strip()
            price = self._parse_price(price_text)

            if price is None:
                return None

            # Extrair URL do produto
            product_link = element.find("a", class_="product-link")
            product_url = product_link["href"] if product_link else ""

            # Extrair brand e model (simplificado)
            brand, model = self._parse_brand_model(title)

            # Verificar estoque
            in_stock = "fora de estoque" not in title.lower()

            # Criar objeto Product
            product = Product(
                name=title,
                category="eletrônico",
                brand=brand,
                model=model,
                specifications={"source": "Kabum"},
            )

            # Adicionar preço
            price_obj = ProductPrice(
                store_name="Kabum",
                price=price,
                in_stock=in_stock,
                product_url=product_url,
            )
            product.add_price(price_obj)

            logger.debug(f"Produto parsed: {product}")
            return product

        except Exception as e:
            logger.error(f"Erro ao fazer parse do produto: {e}")
            return None

    @staticmethod
    def _parse_price(price_text: str) -> Optional[float]:
        """
        Extrai o valor numérico do preço.

        Args:
            price_text: Texto do preço (ex: "R$ 1.299,99")

        Returns:
            Valor em float ou None
        """
        try:
            # Remover "R$" e espaços
            clean = price_text.replace("R$", "").strip()
            # Substituir separador decimal e milhar
            clean = clean.replace(".", "").replace(",", ".")
            return float(clean)
        except (ValueError, AttributeError):
            logger.warning(f"Não consegui fazer parse do preço: {price_text}")
            return None

    @staticmethod
    def _parse_brand_model(title: str) -> tuple[str, str]:
        """
        Extrai brand e model do título.

        Args:
            title: Título do produto

        Returns:
            Tupla (brand, model)
        """
        parts = title.split()
        brand = parts[0] if parts else "Desconhecido"
        model = " ".join(parts[1:3]) if len(parts) > 1 else ""
        return brand, model

    def get_product_details(self, product_url: str) -> Optional[Product]:
        """
        Obtém detalhes completos de um produto.

        Args:
            product_url: URL do produto

        Returns:
            Objeto Product com detalhes
        """
        try:
            logger.info(f"Obtendo detalhes: {product_url}")

            soup = self.fetch_page(product_url)
            if not soup:
                return None

            # Implementar lógica de extração de detalhes aqui
            # Por enquanto, retorna um placeholder

            return None

        except Exception as e:
            logger.error(f"Erro ao obter detalhes do produto: {e}")
            return None


# Exemplo de uso
if __name__ == "__main__":
    scraper = KabumScraper()
    results = scraper.search_products("processador intel i5")
    
    for product in results:
        print(product)
        for price in product.prices:
            print(f"  {price}")
    
    scraper.close()
