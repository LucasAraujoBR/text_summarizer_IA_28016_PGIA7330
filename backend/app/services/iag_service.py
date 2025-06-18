from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from app.models.schemas import AnaliseOutput
from app.core.config import settings

class IAGService:
    """
    Serviço para consumir a API Gemini via Langchain de forma async,
    gerando resumos simples e claros para estudantes.
    """

    def __init__(self):
        self.client = ChatGoogleGenerativeAI(api_key=settings.google_api_key)

    async def processar_analise(self, texto: str) -> AnaliseOutput:
        prompt = (
            "Você é um assistente que cria resumos em português, simples e claros, "
            "para facilitar o entendimento de estudantes que têm dificuldades de leitura. "
            "Se o texto estiver em outra língua, traduza para o português antes de resumir. "
            "Evite termos técnicos complexos, use linguagem acessível.\n\n"
            f"Texto original:\n{texto}\n\n"
            "Retorne apenas o resumo simplificado em JSON no campo 'resumo'."
        )

        response = await self.client.agenerate(messages=[HumanMessage(content=prompt)])

        content = response.generations[0][0].message.content

        import json
        try:
            data = json.loads(content)
            resumo = data.get("resumo", "")
        except Exception:
            resumo = content[:150] + "..."

        return AnaliseOutput(resumo=resumo, classificacao="")

iag_service = IAGService()

async def processar_analise(texto: str) -> AnaliseOutput:
    return await iag_service.processar_analise(texto)
