import time
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.models.schemas import AnaliseOutput, Metadata
from app.core.config import settings

class IAGService:
    """
    Serviço para consumir a API Gemini via Langchain de forma async,
    gerando resumos simples e claros para estudantes.
    """

    def __init__(self):
        # Determina o modelo baseado no MODEL_PROVIDER
        model = self._get_model_by_provider(settings.model_provider)
        
        self.client = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key
        )

    def _get_model_by_provider(self, provider: str) -> str:
        """Retorna o modelo apropriado baseado no provider."""
        model_mapping = {
            "gemini": "gemini-1.5-flash",
            "gemini-pro": "gemini-1.5-pro",
            "gemini-flash": "gemini-1.5-flash",
            "gemini-1.0": "gemini-1.0-pro",
            "gemini-1.5": "gemini-1.5-flash",
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
            "gemma-3-27b-it": "gemma-3-27b-it"
        }
        return model_mapping.get(provider.lower(), "gemini-1.5-flash")

    def _limpar_resumo(self, content: str) -> str:
        """Limpa o resumo removendo formatação JSON e markdown."""
        # Remove blocos de código markdown
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        
        # Remove quebras de linha extras
        content = content.strip()
        
        # Tenta extrair JSON
        try:
            data = json.loads(content)
            if isinstance(data, dict) and 'resumo' in data:
                return data['resumo'].strip()
            elif isinstance(data, str):
                return data.strip()
        except json.JSONDecodeError:
            pass
        
        # Se não for JSON válido, retorna o conteúdo limpo
        return content

    async def processar_analise(self, texto: str) -> AnaliseOutput:
        inicio = time.time()
        
        prompt = (
            "Você é um assistente que cria resumos em português, simples e claros, "
            "para facilitar o entendimento de estudantes que têm dificuldades de leitura. "
            "Se o texto estiver em outra língua, traduza para o português antes de resumir. "
            "Evite termos técnicos complexos, use linguagem acessível.\n\n"
            f"Texto original:\n{texto}\n\n"
            "Retorne apenas o resumo simplificado, sem formatação JSON ou markdown."
        )

        response = await self.client.ainvoke([HumanMessage(content=prompt)])
        content = response.content

        # Limpa o resumo
        resumo = self._limpar_resumo(content)

        # Se o resumo estiver muito longo, trunca
        if len(resumo) > 500:
            resumo = resumo[:500] + "..."

        tempo_processamento = time.time() - inicio
        
        metadata = Metadata(
            tempo_processamento=tempo_processamento,
            tamanho_original=len(texto),
            tamanho_resumo=len(resumo),
            taxa_compressao=len(resumo) / len(texto) if texto else 0.0
        )

        return AnaliseOutput(
            resumo=resumo, 
            classificacao="", 
            metadata=metadata
        )

iag_service = IAGService()

async def processar_analise(texto: str) -> AnaliseOutput:
    return await iag_service.processar_analise(texto)
