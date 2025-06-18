from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.schemas import AnaliseInput, AnaliseOutput, ResultadoHistorico
from app.services.iag_service import processar_analise
from app.validation.input_validator import InputValidator
from app.validation.output_validator import OutputValidator
from app.db.connection import get_db
from app.db.repository import ResultadoRepository

router = APIRouter(
    prefix="/api/v1",
    tags=["resumos"],
    responses={
        404: {"description": "Endpoint não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)

@router.post(
    "/analise",
    response_model=AnaliseOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Gera resumo automático de texto didático",
    description="""
    Endpoint para geração automática de resumos didáticos utilizando o modelo Gemini.
    
    ## Funcionalidades
    - Análise semântica do texto
    - Geração de resumo otimizado
    - Classificação do conteúdo
    - Armazenamento do histórico
    
    ## Parâmetros
    - `texto`: Texto didático a ser analisado (máx. 10.000 caracteres)
    - `opcoes`: Configurações opcionais do resumo
    
    ## Resposta
    Retorna o resumo gerado com metadados e classificação.
    
    ## Erros
    - 400: Texto inválido ou muito longo
    - 500: Erro interno do servidor
    """,
    responses={
        201: {
            "description": "Resumo gerado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "resumo": "Resumo gerado automaticamente...",
                        "classificacao": "Ensino Médio",
                        "metadata": {
                            "tempo_processamento": 2.5,
                            "tamanho_original": 1000,
                            "tamanho_resumo": 300
                        }
                    }
                }
            }
        }
    }
)
async def analisar_texto(
    dados: AnaliseInput,
    db: AsyncSession = Depends(get_db)
):
    """
    Gera um resumo automático do texto didático fornecido.
    
    Args:
        dados (AnaliseInput): Dados de entrada contendo o texto e opções
        db (AsyncSession): Sessão do banco de dados
        
    Returns:
        AnaliseOutput: Resumo gerado com metadados
        
    Raises:
        HTTPException: Em caso de erro na validação ou processamento
    """
    try:
        # Valida entrada
        InputValidator.validar(dados.texto)

        # Processa análise via Gemini Langchain
        resultado = await processar_analise(dados.texto)

        # Valida o resumo gerado
        OutputValidator.validar(resultado.resumo)

        # Salva resultado no banco
        await ResultadoRepository.salvar(db, dados.texto, resultado.resumo, resultado.classificacao)

        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {e}"
        )

@router.get(
    "/historico",
    response_model=List[ResultadoHistorico],
    summary="Lista histórico de resumos",
    description="""
    Endpoint para consulta do histórico de resumos gerados.
    
    ## Funcionalidades
    - Lista resumos gerados
    - Filtragem por data
    - Paginação de resultados
    
    ## Parâmetros
    - `limit`: Limite de resultados (padrão: 10)
    - `offset`: Deslocamento para paginação
    
    ## Resposta
    Lista de resumos com metadados e timestamps.
    """
)
async def listar_historico(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Lista o histórico de resumos gerados.
    
    Args:
        limit (int): Limite de resultados
        offset (int): Deslocamento para paginação
        db (AsyncSession): Sessão do banco de dados
        
    Returns:
        List[ResultadoHistorico]: Lista de resumos gerados
    """
    return await ResultadoRepository.listar(db, limit, offset)
