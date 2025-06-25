from fastapi import FastAPI
from app.api.routes import router as api_router
from app.utils.logger import setup_logger
from app.core.config import settings
from app.db.init_db import init_db
import asyncio

# Configura o logger
setup_logger()

# Cria a aplicação FastAPI com configurações dinâmicas
app = FastAPI(
    title=settings.app_name,
    description="""
    # API de Geração Automática de Resumos Didáticos

    ## 📝 Descrição
    API desenvolvida para gerar resumos automáticos de textos didáticos utilizando o modelo Gemini via Langchain.
    Focada em apoiar estudantes com dificuldades de leitura ou necessidades especiais.

    ## 🚀 Funcionalidades
    - Geração automática de resumos didáticos
    - Validação de entrada e saída
    - Suporte a múltiplos formatos de texto
    - Personalização de parâmetros de resumo

    ## 🔧 Tecnologias
    - FastAPI
    - Langchain
    - Gemini API
    - PostgreSQL (opcional)

    ## 📚 Endpoints

    ### POST /analise
    Gera um resumo automático do texto didático fornecido.

    **Parâmetros:**
    - `text`: Texto didático a ser resumido
    - `options`: Configurações opcionais do resumo
        - `max_length`: Tamanho máximo do resumo
        - `language`: Idioma do resumo (padrão: pt-BR)

    **Resposta:**
    ```json
    {
        "summary": "Resumo gerado",
        "metadata": {
            "original_length": 1000,
            "summary_length": 300,
            "processing_time": 2.5
        }
    }
    ```

    ## 📊 Métricas
    - Tempo de processamento
    - Tamanho do texto original e resumo
    - Taxa de compressão

    ## ⚠️ Limitações
    - Tamanho máximo do texto: 10.000 caracteres
    - Limite de requisições: 100/min
    - Suporte a idiomas: pt-BR, en-US

    ## 🔄 Versão
    Versão atual: 0.1.0
    """,
    version="0.1.0",
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "resumos",
            "description": "Operações relacionadas à geração de resumos didáticos",
        },
        {
            "name": "validação",
            "description": "Endpoints para validação de textos e resumos",
        },
        {
            "name": "métricas",
            "description": "Endpoints para consulta de métricas e estatísticas",
        }
    ],
    contact={
        "name": "Lucas Araújo",
        "email": "lucas.edson@ufrpe.br",
        "url": "https://github.com/LucasAraujoBR"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

@app.on_event("startup")
async def startup_event():
    """Inicializa o banco de dados na inicialização da aplicação."""
    try:
        await init_db()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar banco de dados: {e}")

# Inclui rotas
app.include_router(api_router)
