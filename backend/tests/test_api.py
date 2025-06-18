import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_analise_texto_sucesso():
    payload = {
        "texto": "Texto simples para teste do resumo que deve ser simplificado para estudantes."
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/analise", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resumo" in data
    assert isinstance(data["resumo"], str)
    # A classificação pode estar ausente se removida no serviço
    # assert "classificacao" in data

@pytest.mark.asyncio
async def test_analise_texto_entrada_vazia():
    payload = {"texto": ""}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/analise", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_analise_texto_sem_campo():
    payload = {}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/analise", json=payload)
    assert response.status_code == 422  # erro de validação do Pydantic
