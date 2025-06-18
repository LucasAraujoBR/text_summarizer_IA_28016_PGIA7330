from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql_models import ResultadoAnalise

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
