from fastapi import FastAPI
from api.routes import clients, webhooks
from api.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mundo Invest - Client Management API",
    description="API para gestão de clientes e integração simulada com Pipefy",
    version="1.0.0"
)

app.include_router(clients.router)
app.include_router(webhooks.router)

@app.get("/health")
def read_root():
    return {"status_code": 200, "message": "ok"}
