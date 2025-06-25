from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ResultadoAnalise(Base):
    """Modelo SQL para armazenar resultados de análise de texto."""
    
    __tablename__ = "resultados_analise"
    
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False, comment="Texto original analisado")
    resumo = Column(Text, nullable=False, comment="Resumo gerado")
    classificacao = Column(String(100), nullable=False, comment="Classificação do conteúdo")
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), comment="Data e hora de criação")
    
    def __repr__(self):
        return f"<ResultadoAnalise(id={self.id}, classificacao='{self.classificacao}')>"
