class OutputValidator:
    @staticmethod
    def validar(resumo: str) -> None:
        if not resumo or not resumo.strip():
            raise ValueError("O resumo gerado está vazio.")
        
        if len(resumo.strip().split()) < 3:
            raise ValueError("O resumo está muito curto e pode estar incorreto.")
