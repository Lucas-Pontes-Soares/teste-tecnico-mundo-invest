from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.models.client import Client
from api.schemas.client import ClientCreate, ClientResponse
from api.services import pipefy_service

router = APIRouter(prefix="/clientes", tags=["Clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.cliente_email == client_data.cliente_email).first()
    if db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    new_client = Client(
        cliente_nome=client_data.cliente_nome,
        cliente_email=client_data.cliente_email,
        tipo_solicitacao=client_data.tipo_solicitacao,
        valor_patrimonio=client_data.valor_patrimonio,
        status="Aguardando Análise"
    )
    
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    pipefy_service.simulate_create_card(new_client)
    
    return new_client
