"""Exemplo de uso dos scrapers."""

from src.scrapers import KabumScraper, TerabyteScraper, PichauScraper
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Demonstra o uso dos scrapers."""
    logger.info("=" * 80)
    logger.info("HardTech - Teste de Múltiplos Scrapers")
    logger.info("=" * 80)

    # Lista de scrapers a testar
    scrapers_config = [
        (KabumScraper, "Kabum"),
        (TerabyteScraper, "Terabyte"),
        (PichauScraper, "Pichau"),
    ]

    query = "processador ryzen 5"

    logger.info(f"\n🔍 Buscando: '{query}'\n")

    todos_produtos = {}

    # Buscar em cada loja
    for scraper_class, store_name in scrapers_config:
        logger.info(f"📍 Buscando em {store_name}...\n")
        
        try:
            with scraper_class() as scraper:
                produtos = scraper.search_products(query)

                if produtos:
                    logger.info(f"✓ Encontrados {len(produtos)} produtos:\n")
                    todos_produtos[store_name] = produtos
                    
                    for i, produto in enumerate(produtos[:5], 1):  # Mostrar apenas os 5 primeiros
                        logger.info(f"  {i}. {produto}")
                        for preco in produto.prices:
                            logger.info(f"     {preco}")
                else:
                    logger.warning(f"❌ Nenhum produto encontrado em {store_name}")
                    todos_produtos[store_name] = []

        except Exception as e:
            logger.error(f"❌ Erro ao buscar em {store_name}: {e}")
            todos_produtos[store_name] = []

        logger.info("\n" + "-" * 80 + "\n")

    # Comparativo de preços
    logger.info("\n" + "=" * 80)
    logger.info("COMPARATIVO DE PREÇOS")
    logger.info("=" * 80 + "\n")

    # Consolidar por nome de produto
    produtos_consolidados = {}

    for store_name, produtos in todos_produtos.items():
        for produto in produtos:
            nome = produto.name
            
            if nome not in produtos_consolidados:
                produtos_consolidados[nome] = {
                    "marca": produto.brand,
                    "precos": {}
                }
            
            if produto.prices:
                preco = produto.get_best_price()
                produtos_consolidados[nome]["precos"][store_name] = preco.price

    # Exibir comparativo
    if produtos_consolidados:
        for i, (nome, info) in enumerate(produtos_consolidados.items(), 1):
            precos = info["precos"]
            
            if len(precos) > 1:  # Mostrar apenas produtos que têm preços em múltiplas lojas
                logger.info(f"{i}. {info['marca']} - {nome}")
                
                precos_sorted = sorted(precos.items(), key=lambda x: x[1])
                
                for loja, preco in precos_sorted:
                    mark = " 💰 MELHOR PREÇO" if preco == precos_sorted[0][1] else ""
                    logger.info(f"   {loja}: R$ {preco:.2f}{mark}")
                
                economia = precos_sorted[-1][1] - precos_sorted[0][1]
                logger.info(f"   💵 Economía: R$ {economia:.2f}\n")

    logger.info("=" * 80)
    logger.info("Teste concluído!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
