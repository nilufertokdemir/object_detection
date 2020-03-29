

from kafka import KafkaProducer
import json
from time import sleep


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),)



for e in range(10):
    data = {'number' : e}
    producer.send('deneme', value=data)
    sleep(5)

