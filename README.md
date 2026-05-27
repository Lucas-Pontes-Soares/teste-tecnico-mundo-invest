# Teste Técnico Mundo Invest - Lucas Pontes Soares

Vaga: Desenvolvedor Backend (Pipefy & AWS)

## 🪪 Sobre Mim

Sou **Lucas Pontes Soares**, **Desenvolvedor Full-Stack Júnior** com quase **2 anos de experiência** em **Node.JS**, **React.JS** e gerenciamento de bancos de dados **SQL**.

Habilidade em automação de processos e desenvolvimento de agentes de **IA**.

Com o objetivo em especializar em **Back-end**, busco posição profissional focado em entregar soluções robustas, otimizar processos e contribuir ativamente para o sucesso da equipe.

### 📞 Contato

- 📞 Celular: (14) 98219-7061
- ✉️ Email: <lucasps.dev@outlook.com>
- 👨‍💼 Linkedin: https://www.linkedin.com/in/lucas-pontes-soares/
- 📚 Portfolio: https://lucas-pontes-soares.github.io/portfolio/

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validação:** Pydantic
- **Containerização:** Docker e Docker Compose
- **Visualização de Dados:** pgAdmin 4
- **Testes:** Pytest

## 🛠️ Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passo a Passo
1. Clone o repositório.
2. Crie um arquivo `.env` na raiz do projeto e copie o conteúdo de `.env.example`.
   ```bash
   cp .env.example .env
   ```
3. Na raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
4. A API estará disponível em: `http://localhost:8000`
5. O Swagger (Documentação Interativa) estará em: `http://localhost:8000/docs`
6. O pgAdmin (Interface do Banco) estará em: `http://localhost:5050`
   - **Login:** `admin@admin.com`
   - **Senha:** `admin`

## 🧪 Como Rodar os Testes
Com os containers rodando, execute:
```bash
docker-compose exec api pytest
```

## 📖 Exemplos de Requisição (cURL)

#### 1. Criar um Cliente
```bash
curl -X 'POST' \

  'http://localhost:8000/clientes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}'
```

### 3. Webhook Pipefy (Simulação)
```bash
curl -X 'POST' \
  'http://localhost:8000/webhooks/pipefy/card-updated' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```

## ☁️ Visão de Produção (AWS)
O que pensei na infraestrutura:

1. **API Gateway & AWS Lambda:**  Eu utilizaria o Lambda para uma escalação automática (serveless), aliada com o API Gateway.
2. **Amazon RDS;** Para o banco de dados, alta disponibilidade.
3. **AWS SQS:** Para o processamento do Webhook. O webhook do Pipefy bateria no API Gateway, que salvaria a mensagem no SQS, por exmeplo o RabbitMQ. Uma Lambda processaria a fila de forma assíncrona, garantido que tudo processe corretamente.
4. **Amazon DynamoDB:** Seria só para o controle de idempotência, pensei pois tem baixíssima laténcia, ótimo para verificações rápidas.