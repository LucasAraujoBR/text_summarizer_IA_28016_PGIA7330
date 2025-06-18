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
- Gemini API
- Docker
- PostgreSQL (opcional)
- Pytest para testes
- Pydantic para validação de dados

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
│   │   └── iag_service.py      # Integração com API Gemini/GPT via Langchain
│   ├── validation/
│   │   ├── input_validator.py  # Validação do texto de entrada
│   │   └── output_validator.py # Validação do resumo gerado
│   ├── models/
│   │   └── schemas.py          # Modelos Pydantic para requests/responses
│   ├── utils/
│   │   └── logger.py           # Configuração de logging
│   └── db/                     # Opcional: acesso a banco/cache
│       └── repository.py       # Repositório para operações de dados
├── tests/
│   ├── test_api.py             # Testes dos endpoints da API
│   ├── test_validation.py      # Testes dos validadores de entrada e saída
│   └── test_services.py        # Testes dos serviços Gemini/GPT
├── requirements.txt            # Dependências do projeto
├── .env                       # Variáveis de ambiente sensíveis
├── Dockerfile                 # Containerização da aplicação
└── docker-compose.yml         # Container com API e banco PostgreSQL (se aplicável)
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

* Python 3.8+
* Docker (opcional, para containerização)
* Conta e credenciais API Gemini/GPT (via Langchain)
* Git

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
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

### Executando com Docker

1. Construa a imagem:
```bash
docker build -t resumo-gemini-api .
```

2. Execute o container:
```bash
docker run -p 8000:8000 --env-file .env resumo-gemini-api
```

Ou com docker-compose:
```bash
docker-compose up -d
```

## 📚 Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints Principais

#### POST `/generate-summary`
Gera um resumo automático do texto didático fornecido.

**Request:**
```json
{
  "text": "Seu texto didático aqui...",
  "options": {
    "max_length": 500,
    "language": "pt-BR"
  }
}
```

**Response:**
```json
{
  "summary": "Resumo gerado automaticamente pelo modelo Gemini.",
  "metadata": {
    "original_length": 1000,
    "summary_length": 300,
    "processing_time": 2.5
  }
}
```

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
- Métricas de performance
- Monitoramento de uso da API
- Rastreamento de erros

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


