# Ferramenta de Geração Automática de Resumos Didáticos com Gemini para Educação Inclusiva

Este projeto consiste em uma aplicação backend desenvolvida em FastAPI que utiliza o modelo de linguagem Gemini (via Langchain) para gerar resumos automáticos de textos didáticos, com foco em apoiar estudantes com dificuldades de leitura ou necessidades especiais.

## 🎯 Objetivos

- Desenvolver uma ferramenta de suporte educacional acessível
- Automatizar a geração de resumos didáticos de alta qualidade
- Facilitar o aprendizado para estudantes com necessidades especiais
- Integrar tecnologias de IA avançadas no contexto educacional

## 🚀 Tecnologias Utilizadas

- Python 3.8+
- FastAPI
- Langchain
- **Google Gemini API** (Modelos configuráveis)
- Docker
- PostgreSQL
- Pytest para testes
- Pydantic para validação de dados

## 🤖 Modelos Gemini Suportados

A aplicação suporta múltiplos modelos do Google Gemini através da configuração `MODEL_PROVIDER` no arquivo `.env`:

### Modelos Disponíveis:
- `gemini-1.5-flash` (padrão) - Rápido e eficiente
- `gemini-1.5-pro` - Mais poderoso e preciso
- `gemini-1.0-pro` - Versão estável
- `gemini-1.5` - Alias para gemini-1.5-flash
- `gemini-pro` - Alias para gemini-1.5-pro
- `gemini-flash` - Alias para gemini-1.5-flash
- `gemini-1.0` - Alias para gemini-1.0-pro
- `gemma-3-27b-it` - Modelo Gemma 3

### Configuração no .env:
```env
MODEL_PROVIDER=gemini-1.5-flash
```

## 📁 Estrutura do Projeto

```plaintext
backend/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação FastAPI
│   ├── api/
│   │   └── routes.py           # Definição dos endpoints HTTP
│   ├── core/
│   │   └── config.py           # Configurações e variáveis de ambiente
│   ├── services/
│   │   └── iag_service.py      # Integração com API Gemini via Langchain
│   ├── validation/
│   │   ├── input_validator.py  # Validação do texto de entrada
│   │   └── output_validator.py # Validação do resumo gerado
│   ├── models/
│   │   ├── schemas.py          # Modelos Pydantic para requests/responses
│   │   └── sql_models.py       # Modelos SQLAlchemy para banco de dados
│   ├── utils/
│   │   └── logger.py           # Configuração de logging
│   └── db/                     # Acesso a banco PostgreSQL
│       ├── connection.py       # Configuração de conexão com banco
│       ├── init_db.py          # Inicialização do banco de dados
│       └── repository.py       # Repositório para operações de dados
├── tests/
│   ├── test_api.py             # Testes dos endpoints da API
│   ├── test_validation.py      # Testes dos validadores de entrada e saída
│   └── test_services.py        # Testes dos serviços Gemini
├── requirements.txt            # Dependências do projeto
├── .env                       # Variáveis de ambiente sensíveis
├── Dockerfile                 # Containerização da aplicação
└── docker-compose.yml         # Container com API e banco PostgreSQL
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

* Python 3.8+
* Docker (opcional, para containerização)
* **Conta Google Cloud e credenciais API Gemini**
* Git

### Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/` com as seguintes configurações:

```env
# Configurações da API
APP_NAME=API - textual summaries
ENVIRONMENT=development
DEBUG=true

# Chaves de serviços externos
GOOGLE_API_KEY=sua_chave_google_aqui
MODEL_PROVIDER=gemini-1.5-flash

# Banco de Dados PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:senha123@db:5432/db_analise
```

### 🔑 Como obter a Google API Key:

1. Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada para o campo `GOOGLE_API_KEY` no `.env`

### Instalação Local

1. Clone o repositório:
```bash
git clone <URL_DO_REPOSITÓRIO>
cd backend
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
# Edite o arquivo .env com suas credenciais
```

5. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

### Executando com Docker

1. Configure o arquivo `.env` com suas credenciais
2. Execute com docker-compose:
```bash
docker-compose up -d
```

A aplicação estará disponível em `http://localhost:8000`

## 📚 Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints Principais

#### POST `/api/v1/analise`
Gera um resumo automático do texto didático fornecido.

**Request:**
```json
{
  "texto": "Seu texto didático aqui...",
  "opcoes": {
    "max_length": 500,
    "language": "pt-BR",
    "nivel_ensino": "medio"
  }
}
```

**Response:**
```json
{
  "resumo": "Resumo gerado automaticamente pelo modelo Gemini configurado.",
  "classificacao": "",
  "metadata": {
    "tempo_processamento": 2.5,
    "tamanho_original": 1000,
    "tamanho_resumo": 300,
    "taxa_compressao": 0.3
  }
}
```

#### GET `/api/v1/historico`
Lista o histórico de resumos gerados.

## 🧪 Testes

Execute os testes automatizados:
```bash
pytest tests/
```

Para cobertura de testes:
```bash
pytest --cov=app tests/
```

## 📊 Métricas e Monitoramento

- Logs detalhados de operações
- Métricas de performance (tempo de processamento)
- Monitoramento de uso da API
- Rastreamento de erros
- Histórico de resumos gerados

## 🔧 Configuração Avançada

### Alterando o Modelo Gemini

Para usar um modelo diferente, altere o `MODEL_PROVIDER` no arquivo `.env`:

```env
# Para usar o modelo mais poderoso
MODEL_PROVIDER=gemini-1.5-pro

# Para usar o modelo mais rápido
MODEL_PROVIDER=gemini-1.5-flash

# Para usar o modelo experimental
MODEL_PROVIDER=gemma-3-27b-it
```

### Configuração do Banco de Dados

O banco PostgreSQL é configurado automaticamente via Docker Compose. Para configuração manual:

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
```

## 📝 Paper Científico

O artigo completo detalhando a metodologia, validação e resultados do projeto está disponível no Overleaf:

➡️ [Projeto Overleaf - Ferramenta de Geração Automática de Resumos Didáticos](https://www.overleaf.com/project/6840d13a7f5042985b6f8296)

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📫 Contato

Lucas Araújo — [lucas.edson@ufrpe.br](mailto:lucas.edson@ufrpe.br)

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para detalhes.


