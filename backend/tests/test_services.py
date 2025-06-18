import pytest
import asyncio
from app.services.iag_service import processar_analise

@pytest.mark.asyncio
async def test_processar_analise_retorna_resumo():
    texto = "Este é um texto longo e complexo que precisa ser resumido para facilitar o entendimento."
    resultado = await processar_analise(texto)

    assert hasattr(resultado, "resumo")
    assert isinstance(resultado.resumo, str)
    assert resultado.resumo != ""

    # assert hasattr(resultado, "classificacao")
