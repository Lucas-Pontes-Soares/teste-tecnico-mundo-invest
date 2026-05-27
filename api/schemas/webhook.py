from pydantic import BaseModel
from datetime import datetime

class PipefyWebhookInput(BaseModel):
    event_id: str
    card_id: str
    cliente_email: str
    timestamp: datetime
