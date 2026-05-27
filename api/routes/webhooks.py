from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.models.client import Client
from api.models.event import ProcessedEvent
from api.schemas.webhook import PipefyWebhookInput
from api.services import pipefy_service

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/pipefy/card-updated")
def process_pipefy_webhook(payload: PipefyWebhookInput, db: Session = Depends(get_db)):
    already_processed = db.query(ProcessedEvent).filter(ProcessedEvent.event_id == payload.event_id).first()
    if already_processed:
        return {"message": "Evento já processado anteriormente (ignorado)"}

    client = db.query(Client).filter(Client.cliente_email == payload.cliente_email).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado no sistema local"
        )

    if client.valor_patrimonio >= 200000:
        priority = "prioridade_alta"
    else:
        priority = "prioridade_normal"

    pipefy_service.simulate_update_card_priority(payload.card_id, priority)

    client.status = "Processado"
    client.prioridade = priority
    
    new_event = ProcessedEvent(event_id=payload.event_id)
    db.add(new_event)
    db.commit()

    return {
        "status": "success",
        "message": "Webhook processado com sucesso",
        "cliente": client.cliente_email,
        "prioridade_definida": priority
    }
