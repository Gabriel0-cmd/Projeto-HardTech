"""Scraper para Amazon Brasil."""

from typing import Optional

from src.models import Product, ProductPrice
from src.utils import setup_logger
from .base_scraper import BaseScraper

logger = setup_logger(__name__)


class AmazonBrasilScraper(BaseScraper):
    """Scraper para produtos da Amazon Brasil."""

    def __init__(self):
        """Inicializa o scraper da Amazon Brasil."""
        super().__init__(
            store_name="Amazon",
            base_url="https://www.amazon.com.br"
        )

    def search_products(self, query: str, category: str = None) -> list[Product]:
        """
        Busca produtos na Amazon Brasil.

        Args:
            query: Termo de busca
            category: Categoria (opcional)

        Returns:
            Lista de produtos encontrados
        """
        products = []

        try:
            # URL de busca da Amazon
            search_url = f"{self.base_url}/s?k={query}"
            logger.info(f"Buscando '{query}' na Amazon...")

            soup = self.fetch_page(search_url)
            if not soup:
                logger.error("Não consegui baixar a página de busca")
                return products

            # Procurar pelos produtos (Amazon usa data-component-type)
            product_elements = soup.find_all("div", {"data-component-type": "s-search-result"})

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
            title_elem = element.find("h2", class_="s-line-clamp-2")
            if not title_elem:
                return None

            title = title_elem.text.strip()

            # Extrair preço
            price_elem = element.find("span", class_="a-price-whole")
            if not price_elem:
                return None

            price_text = price_elem.text.strip()
            price = self._parse_price(price_text)

            if price is None:
                return None

            # Extrair URL do produto
            product_link = element.find("h2").find("a")
            product_url = product_link["href"] if product_link else ""
            
            if product_url and not product_url.startswith("http"):
                product_url = self.base_url + product_url

            # Extrair brand e model
            brand, model = self._parse_brand_model(title)

            # Verificar disponibilidade
            availability = element.find("span", class_="a-size-base")
            in_stock = True
            if availability and "indisponível" in availability.text.lower():
                in_stock = False

            # Criar objeto Product
            product = Product(
                name=title,
                category="eletrônico",
                brand=brand,
                model=model,
                specifications={"source": "Amazon Brasil"},
            )

            # Adicionar preço
            price_obj = ProductPrice(
                store_name="Amazon",
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
            price_text: Texto do preço (ex: "1.299,99")

        Returns:
            Valor em float ou None
        """
        try:
            # Amazon separa inteiros com ponto
            # Remover "R$" se presente
            clean = price_text.replace("R$", "").strip()
            # Substituir separador
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

            return None

        except Exception as e:
            logger.error(f"Erro ao obter detalhes do produto: {e}")
            return None


if __name__ == "__main__":
    scraper = AmazonBrasilScraper()
    results = scraper.search_products("ssd 500gb")
    
    for product in results:
        print(product)
        for price in product.prices:
            print(f"  {price}")
    
    scraper.close()
