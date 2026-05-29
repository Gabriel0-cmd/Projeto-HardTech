# 🏗️ Arquitetura do HardTech

## 📋 Visão Geral

HardTech é um projeto em Python desenvolvido em fases para buscar peças de hardware com melhor custo-benefício. A arquitetura foi projetada para ser modular, extensível e testável.

## 📊 Estrutura de Diretórios

```
Projeto-HardTech/
├── src/                              # Código principal
│   ├── __init__.py
│   ├── config.py                     # Configurações globais
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py                # Modelos Product e ProductPrice
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py          # Classe abstrata BaseScraper
│   │   ├── kabum_scraper.py         # Scraper da Kabum
│   │   ├── terabyte_scraper.py      # (TODO) Scraper da Terabyte
│   │   └── pichau_scraper.py        # (TODO) Scraper da Pichau
│   ├── compatibility/               # (TODO) Validador de compatibilidade
│   ├── database/                    # (TODO) Camada de BD
│   ├── api/                         # (TODO) API REST
│   └── utils/
│       ├── __init__.py
│       └── logger.py                # Sistema de logging
├── tests/                            # Testes unitários
│   ├── __init__.py
│   └── test_scrapers.py             # Testes dos scrapers
├── docs/                             # Documentação
│   └── SCRAPERS.md                  # Guia de scrapers
├── main.py                           # Entry point (menu interativo)
├── example_scraper.py               # Exemplo de uso
├── requirements.txt                 # Dependências
├── pyproject.toml                   # Configuração do projeto
├── .env.example                     # Variáveis de ambiente exemplo
└── README.md                        # README principal
```

## 🔄 Fluxo de Dados

```
┌─────────────────────┐
│   Menu Principal    │
│  (main.py)          │
└──────────┬──────────┘
           │
           ├─→ Busca de Produtos
           │       │
           │       ├─→ KabumScraper
           │       ├─→ TerabyteScraper (TODO)
           │       └─→ PichauScraper (TODO)
           │
           ├─→ Compatibilidade (TODO)
           ├─→ Estoque (TODO)
           ├─→ Lojas Próximas (TODO)
           └─→ Guia Educacional (TODO)
```

## 🔧 Componentes Principais

### 1. **Models** (`src/models/`)
Define as estruturas de dados do projeto:
- `Product`: Representa um produto com múltiplos preços
- `ProductPrice`: Preço de um produto em uma loja específica

### 2. **Scrapers** (`src/scrapers/`)
Web scrapers para coletar dados das lojas:
- `BaseScraper`: Classe abstrata com lógica comum
- `KabumScraper`: Implementação para Kabum
- Mais scrapers a vir...

### 3. **Config** (`src/config.py`)
Centraliza todas as configurações:
- Timeout e retry do scraper
- Lista de lojas
- Categorias de produtos
- Configuração de logging e banco de dados

### 4. **Utils** (`src/utils/`)
Funções auxiliares reutilizáveis:
- `logger.py`: Sistema de logging estruturado

## 📈 Fases de Desenvolvimento

### ✅ Fase 1: Scrapers (CONCLUÍDA)
- [x] Arquitetura de scrapers
- [x] BaseScraper
- [x] KabumScraper
- [x] Modelos de dados
- [x] Testes unitários
- [x] Documentação

### 🔄 Fase 2: Compatibilidade (PRÓXIMO)
- [ ] Validador de compatibilidade
- [ ] Base de conhecimento de componentes
- [ ] Regras de compatibilidade
- [ ] Sugestões de peças compatíveis

### 📦 Fase 3: Banco de Dados
- [ ] Modelo de dados persistente
- [ ] Migrations
- [ ] Cache de preços
- [ ] Histórico de preços

### 🌐 Fase 4: API REST
- [ ] Endpoints de busca
- [ ] Endpoints de compatibilidade
- [ ] Autenticação (opcional)
- [ ] Documentação Swagger

### 💻 Fase 5: Interface
- [ ] Web UI (React/Vue)
- [ ] Mobile (Flutter/React Native)
- [ ] CLI melhorada

## 🧪 Testes

Testes unitários cobrem:
- ✅ Modelos de dados
- ✅ Parser de preços
- ✅ Lógica de busca de menor preço
- ✅ Filtros de estoque

Executar testes:
```bash
pytest tests/ -v
pytest tests/ --cov=src  # Com cobertura
```

## 📦 Dependências Principais

```
requests        - HTTP requests
beautifulsoup4  - Web scraping
lxml            - Parser HTML/XML
python-dotenv   - Variáveis de ambiente
flask           - API web (para depois)
pytest          - Framework de testes
```

## 🚀 Como Executar

### Setup Inicial
```bash
# Clonar e navegar
git clone https://github.com/Gabriel0-cmd/Projeto-HardTech.git
cd Projeto-HardTech

# Criar virtual env
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar variáveis de ambiente
cp .env.example .env
```

### Executar Aplicação
```bash
python main.py
```

### Rodar Testes
```bash
pytest tests/ -v
```

### Exemplo de Scraper
```bash
python example_scraper.py
```

## 🎯 Convenções de Código

- **Linguagem**: Python 3.9+
- **Style**: PEP 8
- **Docstrings**: Google style
- **Type hints**: Obrigatório em funções públicas
- **Logging**: Usar `setup_logger(__name__)`

## 📝 Próximos Passos

1. Implementar scrapers para Terabyte e Pichau
2. Criar validador de compatibilidade
3. Configurar banco de dados
4. Implementar API REST com Flask
5. Criar interface web/mobile

## 📞 Contato

Projeto de TCC - Gabriel
GitHub: https://github.com/Gabriel0-cmd/Projeto-HardTech
