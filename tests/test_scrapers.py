"""Testes unitários para os scrapers."""

import unittest
from src.models import Product, ProductPrice
from src.scrapers import KabumScraper, TerabyteScraper, PichauScraper


class TestProductModel(unittest.TestCase):
    """Testes para o modelo Product."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.product = Product(
            name="Intel Core i5-12400",
            category="processador",
            brand="Intel",
            model="Core i5-12400",
            specifications={"cores": 6, "threads": 12},
        )

    def test_product_creation(self):
        """Testa criação de um produto."""
        self.assertEqual(self.product.name, "Intel Core i5-12400")
        self.assertEqual(self.product.brand, "Intel")
        self.assertEqual(self.product.prices, [])

    def test_add_price(self):
        """Testa adição de preço a um produto."""
        price = ProductPrice(store_name="Kabum", price=1200.00)
        self.product.add_price(price)

        self.assertEqual(len(self.product.prices), 1)
        self.assertEqual(self.product.get_best_price().price, 1200.00)

    def test_get_cheapest_store(self):
        """Testa busca pela loja mais barata."""
        self.product.add_price(ProductPrice(store_name="Kabum", price=1200.00))
        self.product.add_price(ProductPrice(store_name="Terabyte", price=1150.00))
        self.product.add_price(ProductPrice(store_name="Pichau", price=1300.00))

        self.assertEqual(self.product.get_cheapest_store(), "Terabyte")
        self.assertEqual(self.product.get_best_price().price, 1150.00)

    def test_in_stock_filter(self):
        """Testa filtragem de produtos em estoque."""
        self.product.add_price(ProductPrice(store_name="Kabum", price=1200.00, in_stock=True))
        self.product.add_price(ProductPrice(store_name="Terabyte", price=1150.00, in_stock=False))

        in_stock = self.product.get_in_stock_prices()
        self.assertEqual(len(in_stock), 1)
        self.assertEqual(in_stock[0].store_name, "Kabum")


class TestProductPrice(unittest.TestCase):
    """Testes para o modelo ProductPrice."""

    def test_discount_calculation(self):
        """Testa cálculo automático de desconto."""
        price = ProductPrice(
            store_name="Kabum",
            price=1000.00,
            original_price=1200.00,
        )

        self.assertIsNotNone(price.discount_percentage)
        self.assertAlmostEqual(price.discount_percentage, 16.67, places=1)

    def test_price_repr(self):
        """Testa representação em string do preço."""
        price = ProductPrice(
            store_name="Kabum",
            price=1200.00,
            in_stock=True,
        )

        repr_str = repr(price)
        self.assertIn("Kabum", repr_str)
        self.assertIn("1200.00", repr_str)


class TestKabumScraper(unittest.TestCase):
    """Testes para o scraper da Kabum."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.scraper = KabumScraper()

    def test_price_parsing(self):
        """Testa parsing de preço."""
        # Teste com formato brasileiro
        price = self.scraper._parse_price("R$ 1.299,99")
        self.assertAlmostEqual(price, 1299.99, places=2)

        # Teste sem R$
        price = self.scraper._parse_price("999,90")
        self.assertAlmostEqual(price, 999.90, places=2)

    def test_brand_model_parsing(self):
        """Testa parsing de brand e model."""
        brand, model = self.scraper._parse_brand_model("Intel Core i5-12400 LGA1700")
        self.assertEqual(brand, "Intel")
        self.assertEqual(model, "Core i5-12400")

    def tearDown(self):
        """Limpeza após cada teste."""
        self.scraper.close()


class TestTerabyteScraper(unittest.TestCase):
    """Testes para o scraper da Terabyte."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.scraper = TerabyteScraper()

    def test_store_name(self):
        """Testa nome da loja."""
        self.assertEqual(self.scraper.store_name, "Terabyte")

    def test_price_parsing(self):
        """Testa parsing de preço."""
        price = self.scraper._parse_price("R$ 899,99")
        self.assertAlmostEqual(price, 899.99, places=2)

    def test_brand_model_parsing(self):
        """Testa parsing de brand e model."""
        brand, model = self.scraper._parse_brand_model("AMD Ryzen 5 5600X")
        self.assertEqual(brand, "AMD")
        self.assertEqual(model, "Ryzen 5")

    def tearDown(self):
        """Limpeza após cada teste."""
        self.scraper.close()


class TestPichauScraper(unittest.TestCase):
    """Testes para o scraper da Pichau."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.scraper = PichauScraper()

    def test_store_name(self):
        """Testa nome da loja."""
        self.assertEqual(self.scraper.store_name, "Pichau")

    def test_price_parsing(self):
        """Testa parsing de preço."""
        price = self.scraper._parse_price("R$ 2.499,00")
        self.assertAlmostEqual(price, 2499.00, places=2)

    def test_brand_model_parsing(self):
        """Testa parsing de brand e model."""
        brand, model = self.scraper._parse_brand_model("NVIDIA RTX 4060 Ti")
        self.assertEqual(brand, "NVIDIA")
        self.assertEqual(model, "RTX 4060")

    def tearDown(self):
        """Limpeza após cada teste."""
        self.scraper.close()


class TestMultipleStores(unittest.TestCase):
    """Testes para comparação entre múltiplas lojas."""

    def test_compare_prices_across_stores(self):
        """Testa comparação de preços entre lojas."""
        product = Product(
            name="SSD Kingston NV2 500GB",
            category="ssd",
            brand="Kingston",
            model="NV2 500GB",
            specifications={"capacity": "500GB", "interface": "NVMe"},
        )

        # Adicionar preços de diferentes lojas
        product.add_price(ProductPrice(store_name="Kabum", price=289.90, in_stock=True))
        product.add_price(ProductPrice(store_name="Terabyte", price=279.90, in_stock=True))
        product.add_price(ProductPrice(store_name="Pichau", price=299.90, in_stock=False))

        # Verificar melhor preço
        self.assertEqual(product.get_cheapest_store(), "Terabyte")
        self.assertEqual(product.get_best_price().price, 279.90)

        # Verificar produtos em estoque
        in_stock = product.get_in_stock_prices()
        self.assertEqual(len(in_stock), 2)


if __name__ == "__main__":
    unittest.main()
