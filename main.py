#!/usr/bin/env python3
"""
HardTech - App de busca de peças de hardware mais baratas
Projeto de TCC - Busca de compatibilidade, preços e confiabilidade
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.scrapers import (
    KabumScraper,
    TerabyteScraper,
    PichauScraper,
    AmazonBrasilScraper,
    MercadoLivreScraper,
    NeweggBrasilScraper,
)
from src.utils import setup_logger

logger = setup_logger(__name__)

# Mapa de scrapers disponíveis
SCRAPERS = {
    "1": ("Kabum", KabumScraper),
    "2": ("Terabyte", TerabyteScraper),
    "3": ("Pichau", PichauScraper),
    "4": ("Amazon", AmazonBrasilScraper),
    "5": ("Mercado Livre", MercadoLivreScraper),
    "6": ("Newegg", NeweggBrasilScraper),
    "0": ("Todas as lojas", None),
}


def display_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 60)
    print("HardTech - Busca de Peças de Hardware")
    print("=" * 60)
    print("\n📋 Menu Principal:")
    print("  1. 🔍 Buscar peças mais baratas")
    print("  2. 🔗 Verificar compatibilidade (em breve)")
    print("  3. 📦 Consultar estoque (em breve)")
    print("  4. 🏪 Lojas próximas (em breve)")
    print("  5. 📚 Guia educacional (em breve)")
    print("  0. ❌ Sair")
    print("=" * 60)


def display_store_menu():
    """Exibe menu de seleção de lojas."""
    print("\n" + "-" * 60)
    print("🏪 Selecione a loja:")
    print("  1. Kabum")
    print("  2. Terabyte")
    print("  3. Pichau")
    print("  0. Todas as lojas")
    print("-" * 60)


def search_products():
    """Busca produtos nas lojas."""
    query = input("\n🔎 Digite o que deseja buscar (ex: 'processador intel i5'): ").strip()

    if not query:
        print("❌ Busca vazia!")
        return

    display_store_menu()
    store_choice = input("Escolha a loja: ").strip()

    if store_choice not in SCRAPERS:
        print("❌ Opção inválida!")
        return

    store_name, scraper_class = SCRAPERS[store_choice]
    
    if store_choice == "0":
        # Buscar em todas as lojas
        search_all_stores(query)
    else:
        # Buscar em uma loja específica
        search_single_store(query, scraper_class, store_name)


def search_single_store(query: str, scraper_class, store_name: str):
    """Busca em uma loja específica."""
    print(f"\n🔍 Buscando '{query}' em {store_name}...\n")

    try:
        with scraper_class() as scraper:
            produtos = scraper.search_products(query)

            if produtos:
                print(f"✓ Encontrados {len(produtos)} produtos:\n")
                for i, produto in enumerate(produtos, 1):
                    print(f"{i}. {produto}")
                    for preco in produto.prices:
                        print(f"   {preco}")
                    print()
            else:
                print("❌ Nenhum produto encontrado")

    except Exception as e:
        logger.error(f"Erro durante busca: {e}")
        print(f"❌ Erro ao buscar: {e}")


def search_all_stores(query: str):
    """Busca em todas as lojas e compara preços."""
    print(f"\n🔍 Buscando '{query}' em todas as lojas...\n")

    produtos_por_loja = {}
    
    for choice, (store_name, scraper_class) in SCRAPERS.items():
        if choice == "0":
            continue
            
        try:
            print(f"  🔄 Buscando em {store_name}...")
            with scraper_class() as scraper:
                produtos = scraper.search_products(query)
                produtos_por_loja[store_name] = produtos
        except Exception as e:
            logger.error(f"Erro ao buscar em {store_name}: {e}")
            produtos_por_loja[store_name] = []

    # Consolidar resultados
    if not any(produtos_por_loja.values()):
        print("\n❌ Nenhum produto encontrado em nenhuma loja")
        return

    print("\n" + "=" * 80)
    print("COMPARATIVO DE PREÇOS")
    print("=" * 80 + "\n")

    # Agrupar produtos por nome
    produtos_consolidados = {}
    
    for store_name, produtos in produtos_por_loja.items():
        for produto in produtos:
            chave = produto.name
            if chave not in produtos_consolidados:
                # Copiar o primeiro produto
                produtos_consolidados[chave] = {
                    "nome": produto.name,
                    "marca": produto.brand,
                    "precos": {}
                }
            
            if produto.prices:
                preco = produto.get_best_price()
                produtos_consolidados[chave]["precos"][store_name] = preco

    # Exibir resultados consolidados
    for i, (nome, info) in enumerate(produtos_consolidados.items(), 1):
        print(f"{i}. {info['marca']} - {info['nome']}")
        
        precos_sorted = sorted(
            info["precos"].items(),
            key=lambda x: x[1].price
        )
        
        for loja, preco in precos_sorted:
            mark = "💰 MELHOR" if preco == precos_sorted[0][1] else ""
            print(f"   {loja}: R$ {preco.price:.2f} {mark}")
        
        economia = precos_sorted[-1][1].price - precos_sorted[0][1].price
        print(f"   💵 Economia: R$ {economia:.2f}\n")


def main():
    """Função principal."""
    logger.info("HardTech iniciado")

    while True:
        display_menu()
        choice = input("\nEscolha uma opção: ").strip()

        if choice == "1":
            search_products()
        elif choice == "2":
            print("\n🔄 Compatibilidade - Em desenvolvimento...")
        elif choice == "3":
            print("\n🔄 Estoque - Em desenvolvimento...")
        elif choice == "4":
            print("\n🔄 Lojas próximas - Em desenvolvimento...")
        elif choice == "5":
            print("\n🔄 Guia educacional - Em desenvolvimento...")
        elif choice == "0":
            print("\n👋 Até logo!")
            logger.info("HardTech encerrado")
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()
