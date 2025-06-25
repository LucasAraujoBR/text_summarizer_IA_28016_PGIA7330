from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sql_models import ResultadoAnalise
from app.models.schemas import ResultadoHistorico
from typing import List

class ResultadoRepository:

    @staticmethod
    async def salvar(db: AsyncSession, texto: str, resumo: str, classificacao: str):
        novo = ResultadoAnalise(
            texto=texto,
            resumo=resumo,
            classificacao=classificacao
        )
        db.add(novo)
        await db.commit()
        await db.refresh(novo)
        return novo

    @staticmethod
    async def listar(db: AsyncSession, limit: int = 10, offset: int = 0) -> List[ResultadoHistorico]:
        query = select(ResultadoAnalise).order_by(ResultadoAnalise.criado_em.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        registros = result.scalars().all()
        
        return [
            ResultadoHistorico(
                id=reg.id,
                texto_original=reg.texto,
                resumo=reg.resumo,
                classificacao=reg.classificacao,
                metadata={
                    "tempo_processamento": 0.0,  # Placeholder
                    "tamanho_original": len(reg.texto),
                    "tamanho_resumo": len(reg.resumo),
                    "taxa_compressao": len(reg.resumo) / len(reg.texto) if reg.texto else 0.0
                },
                criado_em=reg.criado_em
            )
            for reg in registros
        ]
