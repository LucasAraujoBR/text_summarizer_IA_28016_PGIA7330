import pytest
from app.validation.input_validator import InputValidator
from app.validation.output_validator import OutputValidator
from fastapi import HTTPException

def test_input_validator_valido():
    texto = "Texto válido para análise."
    try:
        InputValidator.validar(texto)
    except Exception:
        pytest.fail("InputValidator levantou exceção para texto válido")

def test_input_validator_invalido():
    with pytest.raises(ValueError):
        InputValidator.validar("")

def test_output_validator_valido():
    resumo = "Resumo simples."
    try:
        OutputValidator.validar(resumo)
    except Exception:
        pytest.fail("OutputValidator levantou exceção para resumo válido")

def test_output_validator_invalido():
    with pytest.raises(ValueError):
        OutputValidator.validar("")
