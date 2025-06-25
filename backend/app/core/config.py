from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Configurações da API
    app_name: str = Field("API - textual summaries", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")

    # Chaves de serviços externos
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    model_provider: str = Field("gemini", env="MODEL_PROVIDER")  # Ex: "openai", "gemini"

    # db
    database_url: str = Field(
        "postgresql+asyncpg://user:senha123@db:5432/db_analise", 
        env="DATABASE_URL"
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "protected_namespaces": ("settings_",)
    }

# Instância global para importar em outros módulos
settings = Settings()
