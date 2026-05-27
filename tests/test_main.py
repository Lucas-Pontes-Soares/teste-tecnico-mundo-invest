import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app
from api.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_client_success(client):
    """ Criação de cliente com payload válido"""
    payload = {
        "cliente_nome": "Teste Testador",
        "cliente_email": "teste@exemplo.com",
        "tipo_solicitacao": "Abertura de Conta",
        "valor_patrimonio": 150000
    }
    response = client.post("/clientes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["cliente_nome"] == "Teste Testador"
    assert data["status"] == "Aguardando Análise"

def test_webhook_priority_high(client):
    """ Regra de prioridade alta (>= 200k)"""
    client.post("/clientes/", json={
        "cliente_nome": "Rico",
        "cliente_email": "rico@exemplo.com",
        "tipo_solicitacao": "Investimento",
        "valor_patrimonio": 300000
    })
    
    webhook_payload = {
        "event_id": "evt_high",
        "card_id": "card_high",
        "cliente_email": "rico@exemplo.com",
        "timestamp": "2026-05-25T20:00:00Z"
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    assert response.json()["prioridade_definida"] == "prioridade_alta"

def test_webhook_priority_normal(client):
    """Regra de prioridade normal (< 200k)"""
    client.post("/clientes/", json={
        "cliente_nome": "Normal",
        "cliente_email": "normal@exemplo.com",
        "tipo_solicitacao": "Dúvida",
        "valor_patrimonio": 50000
    })
    
    webhook_payload = {
        "event_id": "evt_normal",
        "card_id": "card_normal",
        "cliente_email": "normal@exemplo.com",
        "timestamp": "2026-05-25T20:00:00Z"
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    assert response.json()["prioridade_definida"] == "prioridade_normal"

def test_webhook_idempotency(client):
    """Bloqueio de event_id duplicado"""
    client.post("/clientes/", json={
        "cliente_nome": "Joao",
        "cliente_email": "joao@exemplo.com",
        "tipo_solicitacao": "Update",
        "valor_patrimonio": 100000
    })
    
    webhook_payload = {
        "event_id": "evt_duplicate",
        "card_id": "card_123",
        "cliente_email": "joao@exemplo.com",
        "timestamp": "2026-05-25T20:00:00Z"
    }
    
    resp1 = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert resp1.status_code == 200
    
    resp2 = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert resp2.status_code == 200
    assert "já processado" in resp2.json()["message"]
