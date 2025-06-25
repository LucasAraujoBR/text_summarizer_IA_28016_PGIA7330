import asyncio
from app.models.sql_models import Base
from app.db.connection import engine

async def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(init_db())
