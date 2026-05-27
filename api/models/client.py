from sqlalchemy import Column, Integer, String, Float
from api.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, nullable=False)
    cliente_email = Column(String, unique=True, index=True, nullable=False)
    tipo_solicitacao = Column(String, nullable=False)
    valor_patrimonio = Column(Float, nullable=False)
    status = Column(String, default="Aguardando Análise")
    prioridade = Column(String, nullable=True)
