import time
import json
import random
from faker import Faker
from datetime import datetime
from kafka import KafkaProducer

# 1. Configura o Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    api_version=(0, 10, 1)
)

fake = Faker('pt_BR')

def gerar_leitura_sensor():
    tipo_regiao = random.choice(['URBANA', 'RURAL'])
    
    # 95% normal, 5% apagão
    status_rede = random.choices(['NORMAL', 'APAGAO'], weights=[95, 5])[0]
    
    if status_rede == 'NORMAL':
        voltagem = random.choice([110.5, 127.2, 219.8, 220.1])
    else:
        voltagem = 0.0

    dados = {
        "id_medidor": fake.uuid4(),
        "cliente": fake.name(),
        "endereco": fake.address(),
        "bairro": fake.bairro(),
        "regiao": tipo_regiao,
        "voltagem": voltagem,
        "timestamp": datetime.now().isoformat()
    }
    return dados

print("INICIANDO ENVIO PARA O GUARDIAN GRID")
print("Pressione CTRL+C para parar...")

try:
    while True:
        evento = gerar_leitura_sensor()
        
        # 2.  Envia pro Tópico 'medidor-energia'
        producer.send('medidor-energia', value=evento)
        
        # Imprime na tela pra checar o funcionamento
        if evento['voltagem'] == 0:
            print(f"ENVIADO APAGÃO: {evento['cliente']}")
        else:
            print(f"Enviado leitura normal: {evento['cliente']}")
            
        time.sleep(1) # Um envio por segundo

except KeyboardInterrupt:
    print("\n Parando simulação...")
