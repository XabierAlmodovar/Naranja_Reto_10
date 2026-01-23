import joblib
import pandas as pd
import json
import time
import random
from confluent_kafka import Producer

# Configuración de Kafka
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Error: {err}")

if __name__ == "__main__":
    TOPIC = 'prenda_nueva'

    print("Cargando grafo desde .pkl...")
    try:
        G = joblib.load('grafo_season9.pkl')#grafo
        print("Enviando aristas del grafo a Kafka...")
        for u, v, data in G.edges(data=True):
            mensaje_grafo = {
                "tipo": "ESTRUCTURA_GRAFO",
                "item_a": u,
                "item_b": v,
                "peso": data.get('weight', 1.0)
            }
            producer.produce(TOPIC, value=json.dumps(mensaje_grafo).encode('utf-8'), callback=delivery_report)
        producer.flush()
        print("Estructura del grafo enviada.")
    except Exception as e:
        print(f"Error con el PKL: {e}")

    print("\nLeyendo prendas desde CSV...")
    try:
        df_prendas = pd.read_csv("../Datos/Transformados/Season9_limpios.csv")
        prenda_escogida = random.choice(df_prendas['indice'].tolist())

        
        mensaje_prediccion = {
            "tipo": "SOLICITUD_PREDICCION",
            "item_objetivo": prenda_escogida
        }
        
        producer.produce(TOPIC, value=json.dumps(mensaje_prediccion).encode('utf-8'), callback=delivery_report)
        producer.flush()
        print(f"Enviada solicitud para combinar: {prenda_escogida}")
    except Exception as e:
        print(f"Error con el CSV: {e}")
