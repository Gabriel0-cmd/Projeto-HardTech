# 🔍 Guia de Scrapers - HardTech

## Visão Geral

Os scrapers são responsáveis por buscar dados de preços e produtos das lojas online de hardware. O sistema foi desenvolvido com uma arquitetura extensível para permitir adicionar novas lojas facilmente.

## Lojas Suportadas

Atualmente, o HardTech suporta os seguintes scrapers:

| Loja | Status | Classe |
|------|--------|--------|
| 🟢 Kabum | Funcional | `KabumScraper` |
| 🟢 Terabyte | Funcional | `TerabyteScraper` |
| 🟢 Pichau | Funcional | `PichauScraper` |

## Arquitetura

```
scrapers/
├── __init__.py
├── base_scraper.py      # Classe abstrata base
├── kabum_scraper.py     # Implementação para Kabum
├── terabyte_scraper.py  # Implementação para Terabyte
└── pichau_scraper.py    # Implementação para Pichau
```

## BaseScraper

Classe abstrata que define a interface para todos os scrapers:

### Métodos principais:

- **`fetch_page(url: str) -> BeautifulSoup`**: Baixa e faz parse de uma página HTML
  - Implementa retry automático
  - Respeita delays entre requisições
  - Trata timeouts e erros

- **`search_products(query: str, category: str = None) -> list[Product]`**: Busca produtos
  - Deve ser implementado por cada scraper específico
  - Retorna lista de objetos Product

- **`get_product_details(product_url: str) -> Product`**: Obtém detalhes completos
  - Deve ser implementado por cada scraper específico
  - Retorna objeto Product com informações completas

### Configuração

```python
SCRAPER_CONFIG = {
    "timeout": 10,              # Timeout em segundos
    "retries": 3,               # Número de tentativas
    "delay": 1.0,               # Delay entre requisições
    "user_agent": "Mozilla/5.0...",
}
```

## Usando um Scraper

### Exemplo Básico

```python
from src.scrapers import KabumScraper

# Context manager (recomendado)
with KabumScraper() as scraper:
    produtos = scraper.search_products("processador intel i5")
    
    for produto in produtos:
        print(f"{produto.name} - {produto.get_best_price()}")
```

### Exemplo Avançado

```python
from src.scrapers import KabumScraper

scraper = KabumScraper()

try:
    # Buscar produtos
    produtos = scraper.search_products("placa mãe B760")
    
    # Filtrar por estoque
    em_estoque = [p for p in produtos if p.get_in_stock_prices()]
    
    # Ordenar por preço
    ordenado = sorted(em_estoque, key=lambda p: p.get_best_price().price)
    
    # Exibir resultados
    for i, produto in enumerate(ordenado[:5], 1):
        print(f"{i}. {produto}")
        print(f"   Melhor preço: R$ {produto.get_best_price().price:.2f}")
        print(f"   Loja: {produto.get_cheapest_store()}")
        
finally:
    scraper.close()
```

## Modelo de Dados

### Product

```python
@dataclass
class Product:
    name: str                          # Nome do produto
    category: str                      # Categoria (processador, placa-mãe, etc)
    brand: str                         # Marca (Intel, AMD, etc)
    model: str                         # Modelo específico
    specifications: dict               # Especificações (cores, threads, etc)
    prices: list[ProductPrice] = None  # Preços em diferentes lojas
```

#### Métodos úteis:

- `add_price(price: ProductPrice)`: Adiciona um preço
- `get_best_price() -> ProductPrice`: Retorna o preço mais baixo
- `get_cheapest_store() -> str`: Retorna o nome da loja mais barata
- `get_in_stock_prices() -> list[ProductPrice]`: Retorna apenas preços em estoque

### ProductPrice

```python
@dataclass
class ProductPrice:
    store_name: str                    # Nome da loja (Kabum, Terabyte, etc)
    price: float                       # Preço atual em reais
    original_price: Optional[float]    # Preço original (se houver desconto)
    discount_percentage: Optional[float]  # Percentual de desconto
    in_stock: bool = True              # Se está em estoque
    product_url: str = ""              # URL do produto na loja
    scraped_at: datetime               # Data/hora do scraping
```

## Implementando um Novo Scraper

Para adicionar uma nova loja, siga este exemplo:

### 1. Criar o arquivo `src/scrapers/nova_loja_scraper.py`

```python
from src.scrapers import BaseScraper
from src.models import Product, ProductPrice

class NovaLojaScaper(BaseScraper):
    """Scraper para a loja NovaLoja."""
    
    def __init__(self):
        super().__init__(
            store_name="NovaLoja",
            base_url="https://www.novaloja.com.br"
        )
    
    def search_products(self, query: str, category: str = None) -> list[Product]:
        """Implementar busca de produtos."""
        # 1. Montar URL de busca
        # 2. Baixar página com self.fetch_page()
        # 3. Fazer parse do HTML
        # 4. Extrair informações de cada produto
        # 5. Retornar lista de Product
        pass
    
    def get_product_details(self, product_url: str) -> Product:
        """Implementar extração de detalhes."""
        pass
```

### 2. Adicionar à lista de lojas em `src/config.py`

```python
STORES = {
    "novaloja": {
        "name": "NovaLoja",
        "url": "https://www.novaloja.com.br",
        "enabled": True,
    },
}
```

### 3. Exportar em `src/scrapers/__init__.py`

```python
from .nova_loja_scraper import NovaLojaScaper

__all__ = ["BaseScraper", "KabumScraper", "NovaLojaScaper"]
```

## Testes

Os scrapers incluem testes unitários. Para rodar:

```bash
pytest tests/test_scrapers.py -v

# Com cobertura
pytest tests/test_scrapers.py --cov=src.scrapers
```

## Boas Práticas

1. **Respeite o servidor**: Use delays apropriados entre requisições
2. **Trate erros**: Sempre use try/except para requisições HTTP
3. **Log detalhado**: Use o logger para debug
4. **Context manager**: Use `with` para garantir limpeza de recursos
5. **Cache**: Considere cachear resultados para evitar re-scraping

## Limitações Conhecidas

- Alguns sites bloqueiam web scrapers
- Estrutura HTML pode mudar e quebrar seletores
- Rate limiting pode ocorrer com muitas requisições
- Alguns sites requerem JavaScript (não suportado por BeautifulSoup)

## Próximos Passos

- [ ] Implementar scrapers para Terabyte e Pichau
- [ ] Adicionar suporte a JavaScript (Selenium/Playwright)
- [ ] Implementar cache com Redis
- [ ] Adicionar notificações de mudança de preço
- [ ] Crawler de compatibilidade
