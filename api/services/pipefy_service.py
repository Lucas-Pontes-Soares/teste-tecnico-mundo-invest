from api.models.client import Client

def simulate_create_card(client: Client):
    
    mutation = f"""
    mutation {{
      createCard(input: {{
        pipe_id: "SEU_PIPE_ID",
        fields_attributes: [
          {{ field_id: "nome_do_cliente", field_value: "{client.cliente_nome}" }},
          {{ field_id: "email_do_cliente", field_value: "{client.cliente_email}" }},
          {{ field_id: "valor_patrimonio", field_value: "{client.valor_patrimonio}" }}
        ]
      }}) {{
        card {{
          id
          title
        }}
      }}
    }}
    """
    
    print("\n" + "="*50)
    print("SIMULANDO ENVIO PARA PIPEFY (GraphQL Mutation):")
    print(mutation)
    print("="*50 + "\n")
    
    return True

def simulate_update_card_priority(card_id: str, priority: str):
    mutation = f"""
    mutation {{
      updateCardField(input: {{
        card_id: "{card_id}",
        field_id: "prioridade",
        new_value: "{priority}"
      }}) {{
        success
        card {{
          id
        }}
      }}
    }}
    """
    
    print("\n" + "="*50)
    print("SIMULANDO UPDATE NO PIPEFY (GraphQL Mutation):")
    print(mutation)
    print("="*50 + "\n")
    
    return True
