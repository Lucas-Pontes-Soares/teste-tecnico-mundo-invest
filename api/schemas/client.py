from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ClientCreate(BaseModel):
    cliente_nome: str = Field(..., min_length=2)
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float = Field(..., gt=0)

class ClientResponse(ClientCreate):
    id: int
    status: str
    prioridade: str | None = None

    model_config = ConfigDict(from_attributes=True)
