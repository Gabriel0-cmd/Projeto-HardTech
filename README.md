# HardTech 💻

**Projeto de TCC** - App inteligente para busca de peças de hardware mais baratas e compatíveis.

## 📋 Sobre o Projeto

HardTech é uma aplicação que ajuda usuários a encontrar peças de computador (hardware) com o melhor preço do mercado, considerando:

✅ **Compatibilidade** - Verifica quais peças são compatíveis entre si
✅ **Preços** - Encontra as peças mais baratas disponíveis
✅ **Estoque** - Mostra disponibilidade em tempo real
✅ **Marcas** - Lista marcas disponíveis e suas características
✅ **Lojas** - Identifica lojas próximas e sua confiabilidade
✅ **Educação** - Explica o que cada peça faz e como escolher a melhor geração

## 🎯 Funcionalidades Principais

### 1. Busca de Peças
- Buscar peças de hardware por tipo, marca, especificação
- Filtrar por faixa de preço
- Ordenar por preço, avaliação, compatibilidade

### 2. Análise de Compatibilidade
- Validar compatibilidade entre componentes
- Alertar sobre incompatibilidades
- Sugerir alternativas compatíveis

### 3. Verificação de Estoque
- Consultar estoque em múltiplas lojas
- Notificar quando produtos ficam disponíveis
- Comparação de preços e estoque

### 4. Informações de Lojas
- Localizar lojas próximas
- Avaliar confiabilidade de lojas
- Histórico de avaliações

### 5. Guia Educacional
- O que cada peça faz (processador, placa-mãe, etc.)
- Diferenças entre gerações de componentes
- Como escolher a melhor relação custo-benefício

## 🛠️ Tecnologias

- **Python 3.9+** - Linguagem principal
- **Flask** - Web framework (backend)
- **BeautifulSoup** - Web scraping
- **Requests** - HTTP requests
- **SQLite/PostgreSQL** - Banco de dados (a definir)

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes)
- git

### Passos

1. **Clonar o repositório**
```bash
git clone https://github.com/Gabriel0-cmd/Projeto-HardTech.git
cd Projeto-HardTech
```

2. **Criar ambiente virtual**
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Executar o aplicativo**
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
Projeto-HardTech/
├── src/                      # Código-fonte principal
│   ├── __init__.py
│   ├── scrapers/             # Webscraping de lojas
│   ├── compatibility/        # Lógica de compatibilidade
│   ├── database/             # Operações com banco de dados
│   ├── api/                  # APIs do aplicativo
│   └── utils/                # Funções auxiliares
├── tests/                    # Testes unitários
├── docs/                     # Documentação
├── main.py                   # Arquivo principal
├── requirements.txt          # Dependências
├── pyproject.toml            # Configuração do projeto
├── .gitignore
└── README.md                 # Este arquivo
```

## 🚀 Próximos Passos

- [ ] Estruturar módulos de scraping
- [ ] Implementar lógica de compatibilidade
- [ ] Criar API REST
- [ ] Desenvolver banco de dados
- [ ] Interface de usuário (CLI/Web)
- [ ] Sistema de notificações

## 👨‍💻 Autor

**Gabriel** - Projeto de TCC

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 📞 Suporte

Para dúvidas ou sugestões, abra uma [issue](https://github.com/Gabriel0-cmd/Projeto-HardTech/issues).