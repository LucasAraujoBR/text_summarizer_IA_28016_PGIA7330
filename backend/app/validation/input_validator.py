class InputValidator:
    @staticmethod
    def validar(texto: str) -> None:
        if not texto or not texto.strip():
            raise ValueError("O texto de entrada está vazio.")
        
        if len(texto.strip()) < 15:
            raise ValueError("O texto deve conter pelo menos 15 caracteres.")
