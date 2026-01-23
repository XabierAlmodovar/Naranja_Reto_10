import joblib
import pandas as pd
import json
from confluent_kafka import Consumer, KafkaException
import sys
import os


conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumer_look_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
TOPIC = 'prenda_nueva'

print("Cargando grafo desde .pkl...")
try:
    G = joblib.load('grafo_season9.pkl')
    print("Grafo cargado correctamente.")
except Exception as e:
    print(f"Error cargando grafo: {e}")
    sys.exit(1)

print("Cargando CSV de prendas...")
try:
    df_prendas = df_nodes = pd.read_csv("../Datos/Transformados/Season9_limpios.csv")
    id_to_title = dict(
        zip(df_prendas['indice'].astype(int), df_prendas['title'].astype(str))
    )
    id_to_color = dict(
    zip(df_prendas['indice'].astype(int), df_prendas['color'].astype(str))
    )
    print("Mapeo ID → title cargado.")
except Exception as e:
    print(f"Error cargando CSV: {e}")
    sys.exit(1)

def obtener_vecinos_mas_cercanos(grafo, nodo, k=2):
    if nodo not in grafo:
        print(f"La prenda {nodo} no está en el grafo.")
        return []

    vecinos = grafo[nodo]
    sorted_neighbors = sorted(
        vecinos.items(),
        key=lambda x: x[1].get('weight', 1.0),
        reverse=True
    )
    return [v[0] for v in sorted_neighbors[:k]]


consumer.subscribe([TOPIC])

print("Esperando solicitudes de predicción...")
  
try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            raise KafkaException(msg.error())

        data = json.loads(msg.value().decode('utf-8'))

        if data.get("tipo") != "SOLICITUD_PREDICCION":
            continue

        try:
            prenda_objetivo = int(data["item_objetivo"])#id viene como str
        except ValueError:
            print(f"ID inválido recibido: {data['item_objetivo']}")
            continue

        vecinos = obtener_vecinos_mas_cercanos(G, prenda_objetivo, k=2)#se genera el look

        if len(vecinos) < 2:
            print(f"No hay suficientes vecinos para {prenda_objetivo}")
            continue

        look_ids = [prenda_objetivo] + vecinos
        #cambiar a titles
        look_titles = [id_to_title.get(i, f"ID_{i}") for i in look_ids]
        look_colors = [id_to_color.get(i, "Unknown") for i in look_ids]
        print("\n LOOK GENERADO")
        print(f"  • Prenda principal : {look_titles[0]} ({look_colors[0]})")
        print(f"  • Combinación 1    : {look_titles[1]} ({look_colors[1]})")
        print(f"  • Combinación 2    : {look_titles[2]} ({look_colors[2]})")
        #guardar csv
        df_look = pd.DataFrame([[
    look_titles[0], look_colors[0],
    look_titles[1], look_colors[1],
    look_titles[2], look_colors[2]
]], columns=[
    'Prenda Principal', 'Color Principal',
    'Combinación 1', 'Color 1',
    'Combinación 2', 'Color 2'
])

        df_look.to_csv(
    'looks_generados.csv',
    mode='a',
    header=not os.path.exists('looks_generados.csv'),
    index=False
)
        print("Look guardado en 'looks_generados.csv'")

except KeyboardInterrupt:
    print("\nCerrando consumer...")

finally:
    consumer.close()

