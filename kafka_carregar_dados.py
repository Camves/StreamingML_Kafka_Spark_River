from kafka import KafkaProducer
import json
import time

x,y,z = 1,1,1

# Função para criar dados fictícios
def create_data():
    global x,y,z
    x = x *1.4
    y = y *1.2
    z = z * 1.3  # Alternar entre 0 e 1 para ter valores de label como binários
    return {'feature1': x, 'feature2': y, 'label': z}

# Criar produtor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Enviar dados para o tópico
for _ in range(1000):  # Enviar 1000 mensagens
    data = create_data()
    producer.send('dados_teste', value=data)
    print("enviado")
    time.sleep(1)  # Esperar 1 segundo entre as mensagens

producer.flush()
