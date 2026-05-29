"""Modelos de dados para produtos e preços."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProductPrice:
    """Representa o preço de um produto em uma loja."""

    store_name: str
    price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    in_stock: bool = True
    product_url: str = ""
    scraped_at: datetime = None

    def __post_init__(self):
        """Inicialização pós-construção."""
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

        # Calcular desconto se não informado
        if (
            self.discount_percentage is None
            and self.original_price
            and self.original_price > self.price
        ):
            self.discount_percentage = (
                (self.original_price - self.price) / self.original_price
            ) * 100

    def __repr__(self):
        status = "✓ Em estoque" if self.in_stock else "✗ Sem estoque"
        discount_str = (
            f" (-{self.discount_percentage:.1f}%)" if self.discount_percentage else ""
        )
        return f"{self.store_name}: R$ {self.price:.2f}{discount_str} [{status}]"


@dataclass
class Product:
    """Representa um produto de hardware."""

    name: str
    category: str
    brand: str
    model: str
    specifications: dict
    prices: list[ProductPrice] = None

    def __post_init__(self):
        """Inicialização pós-construção."""
        if self.prices is None:
            self.prices = []

    def add_price(self, price: ProductPrice):
        """Adiciona um preço para este produto."""
        self.prices.append(price)

    def get_best_price(self) -> Optional[ProductPrice]:
        """Retorna o preço mais baixo disponível."""
        if not self.prices:
            return None
        return min(self.prices, key=lambda p: p.price)

    def get_cheapest_store(self) -> Optional[str]:
        """Retorna o nome da loja com o preço mais baixo."""
        best = self.get_best_price()
        return best.store_name if best else None

    def get_in_stock_prices(self) -> list[ProductPrice]:
        """Retorna apenas preços de produtos em estoque."""
        return [p for p in self.prices if p.in_stock]

    def __repr__(self):
        best_price = self.get_best_price()
        price_str = f"R$ {best_price.price:.2f}" if best_price else "N/A"
        return f"{self.brand} {self.model} - {price_str}"
