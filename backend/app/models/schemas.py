from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime

class OpcoesResumo(BaseModel):
    """Configurações opcionais para geração do resumo."""
    max_length: Optional[int] = Field(
        default=500,
        ge=100,
        le=2000,
        description="Tamanho máximo do resumo em caracteres"
    )
    language: Optional[str] = Field(
        default="pt-BR",
        description="Idioma do resumo (pt-BR ou en-US)"
    )
    nivel_ensino: Optional[str] = Field(
        default="medio",
        description="Nível de ensino do resumo (fundamental, medio, superior)"
    )

    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        """Valida o idioma do resumo."""
        if v not in ["pt-BR", "en-US"]:
            raise ValueError("Idioma deve ser pt-BR ou en-US")
        return v

    @field_validator('nivel_ensino')
    @classmethod
    def validate_nivel_ensino(cls, v):
        """Valida o nível de ensino."""
        if v not in ["fundamental", "medio", "superior"]:
            raise ValueError("Nível de ensino inválido")
        return v

class AnaliseInput(BaseModel):
    """Modelo de entrada para análise de texto."""
    texto: str = Field(
        ...,
        min_length=15,
        max_length=10000,
        description="Texto didático para ser analisado e resumido."
    )
    opcoes: Optional[OpcoesResumo] = Field(
        default=OpcoesResumo(),
        description="Configurações opcionais para geração do resumo"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "A fotossíntese é o processo pelo qual as plantas convertem energia luminosa em energia química, produzindo oxigênio como subproduto. Este processo é fundamental para a vida na Terra, pois é a principal fonte de oxigênio atmosférico.",
                "opcoes": {
                    "max_length": 300,
                    "language": "pt-BR",
                    "nivel_ensino": "medio"
                }
            }
        }
    }

class Metadata(BaseModel):
    """Metadados do processamento."""
    tempo_processamento: float = Field(..., description="Tempo de processamento em segundos")
    tamanho_original: int = Field(..., description="Tamanho do texto original em caracteres")
    tamanho_resumo: int = Field(..., description="Tamanho do resumo em caracteres")
    taxa_compressao: float = Field(..., description="Taxa de compressão do resumo")

class AnaliseOutput(BaseModel):
    """Modelo de saída da análise."""
    resumo: str = Field(..., description="Resumo gerado a partir do texto.")
    classificacao: str = Field(..., description="Classificação do conteúdo (ex: biologia, matemática, etc).")
    metadata: Optional[Metadata] = Field(None, description="Metadados do processamento")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resumo": "Processo de fotossíntese: conversão de energia luminosa em química pelas plantas, gerando oxigênio. Fundamental para a vida na Terra.",
                "classificacao": "biologia",
                "metadata": {
                    "tempo_processamento": 2.5,
                    "tamanho_original": 250,
                    "tamanho_resumo": 150,
                    "taxa_compressao": 0.6
                }
            }
        }
    }

class ResultadoHistorico(BaseModel):
    """Modelo para histórico de resumos."""
    id: int = Field(..., description="ID único do registro")
    texto_original: str = Field(..., description="Texto original analisado")
    resumo: str = Field(..., description="Resumo gerado")
    classificacao: str = Field(..., description="Classificação do conteúdo")
    metadata: Dict[str, Any] = Field(..., description="Metadados do processamento")
    criado_em: datetime = Field(..., description="Data e hora de criação")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "texto_original": "Texto original...",
                "resumo": "Resumo gerado...",
                "classificacao": "biologia",
                "metadata": {
                    "tempo_processamento": 2.5,
                    "tamanho_original": 250,
                    "tamanho_resumo": 150,
                    "taxa_compressao": 0.6
                },
                "criado_em": "2024-02-20T10:30:00"
            }
        }
    }
