import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# 1. Conexão com o Banco de Dados (MongoDB)
# 27017 é a porta padrão do MongoDB via Docker
try:
    client_mongo = MongoClient('mongodb://localhost:27017/')
    db = client_mongo['guardian_grid'] # Nome do Banco
    colecao = db['leituras_sensor']    # Nome da Coleção
    print("Conectado ao MongoDB com sucesso!")
except Exception as e:
    print(f"Erro ao conectar no Mongo: {e}")

# 2. Configura o Kafka Consumer
consumer = KafkaConsumer(
    'medidor-energia',                 # O mesmo tópico do produtor
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',      # Começa do início da fila
    enable_auto_commit=True,           # Marca como lido automaticamente
    group_id='grupo-arquivistas',      # Identidade do grupo de consumidores
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    api_version=(0, 10, 1)             # Compatibilidade com a versão do Kafka
)

print("AGENTE ARQUIVO: Ouvindo a esteira do Kafka...")
print("Aguardando dados... (Pressione CTRL+C para sair)")

# 3. O Loop Infinito 
for mensagem in consumer:
    leitura = mensagem.value
    
    # Salva no MongoDB
    try:
        colecao.insert_one(leitura)
        
        # Feedback visual no console
        cliente = leitura.get('cliente', 'Desconhecido')
        voltagem = leitura.get('voltagem')
        
        if voltagem == 0:
            print(f"APAGÃO REGISTRADO NO BANCO: {cliente}")
        else:
            print(f"Salvo: {cliente} | {voltagem}V")
            
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
