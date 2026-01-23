import threading
import time
import json
import os
import joblib
import pandas as pd
from flask import Flask, request, render_template_string
from confluent_kafka import Producer, Consumer, KafkaException


TOPIC = 'prenda_nueva'

KAFKA_CONF_PRODUCER = {
    'bootstrap.servers': 'localhost:9092'
}

KAFKA_CONF_CONSUMER = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumer_app_group',
    'auto.offset.reset': 'latest'
}

producer = Producer(KAFKA_CONF_PRODUCER)


print("Cargando grafo y datos...")

G = joblib.load('grafo_season9.pkl')
df_prendas = pd.read_csv("../Datos/Transformados/Season9_limpios.csv")

id_to_title = dict(zip(df_prendas['indice'].astype(int), df_prendas['title']))
id_to_type = {
    idx: title.split()[1] if len(title.split()) > 1 else title.split()[0]
    for idx, title in zip(df_prendas['indice'].astype(int), df_prendas['title'])
}


prendas_validas = [
    idx for idx in df_prendas['indice']
    if idx in G and len(G[idx]) >= 2
]

if len(prendas_validas) >= 30:
    df_30 = df_prendas[df_prendas['indice'].isin(prendas_validas)].sample(30, random_state=42)
else:
    df_30 = df_prendas[df_prendas['indice'].isin(prendas_validas)]

#función para obtener los vecinos

def obtener_vecinos_mas_cercanos(grafo, nodo, k=2):
    if nodo not in grafo:
        return []

    vecinos = grafo[nodo]
    vecinos_ordenados = sorted(
        vecinos.items(),
        key=lambda x: x[1].get('weight', 1.0),
        reverse=True
    )

    vecinos_limpios = []
    tipo_objetivo = id_to_type.get(nodo)

    for v_id, _ in vecinos_ordenados:
        tipo_vecino = id_to_type.get(v_id)
        if v_id != nodo and tipo_vecino != tipo_objetivo:
            vecinos_limpios.append(v_id)
        if len(vecinos_limpios) == k:
            break

    return vecinos_limpios

csv_path = 'looks_generados.csv'

if not os.path.exists(csv_path):
    pd.DataFrame(
        columns=['Prenda Objetivo', 'Vecino 1', 'Vecino 2', 'item_objetivo']
    ).to_csv(csv_path, index=False)

def consumer_loop():
    consumer = Consumer(KAFKA_CONF_CONSUMER)
    consumer.subscribe([TOPIC])

    print("Consumer ejecutándose...")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            raise KafkaException(msg.error())

        data = json.loads(msg.value().decode('utf-8'))

        if data.get("tipo") != "SOLICITUD_PREDICCION":
            continue

        prenda_id = int(data["item_objetivo"])
        vecinos = obtener_vecinos_mas_cercanos(G, prenda_id)

        if len(vecinos) < 2:
            print(f"Prenda {prenda_id} sin suficientes combinaciones")
            continue

        look_ids = [prenda_id] + vecinos
        look_titles = [id_to_title[i] for i in look_ids]

        df_look = pd.DataFrame(
            [[look_titles[0], look_titles[1], look_titles[2], prenda_id]],
            columns=['Prenda Objetivo', 'Vecino 1', 'Vecino 2', 'item_objetivo']
        )

        if os.path.exists(csv_path):
            df_old = pd.read_csv(csv_path)
            df_final = pd.concat([df_old, df_look], ignore_index=True)
        else:
            df_final = df_look

        df_final.to_csv(csv_path, index=False)

        print("Look generado:", look_titles)


app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Recomendador de Looks</title>
<style>
    body { 
        font-family: 'Segoe UI', Arial, sans-serif; 
        background-color: #FFF0F5; /* Rosa clarito clarito */
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    .card { 
        max-width: 600px; 
        width: 90%;
        background: white; 
        padding: 40px; 
        border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
    }
    h1 { color: #444; margin-bottom: 25px; }
    select { 
        width: 100%; 
        padding: 12px; 
        border-radius: 10px; 
        border: 1px solid #ddd; 
        font-size: 16px;
        margin-bottom: 20px;
    }
    button { 
        background: #F06C7A; 
        color: white; 
        padding: 15px; 
        border: none; 
        width: 100%; 
        border-radius: 12px; 
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    button:hover { background: #d95b68; }
    .result-box {
        margin-top: 30px;
        padding: 20px;
        background: #fdf2f3;
        border-radius: 15px;
        text-align: left;
    }
    ul { list-style: none; padding: 0; }
    li { padding: 8px 0; border-bottom: 1px solid #eee; color: #555; }
    .warning { margin-top:30px; padding:20px; background:#FFF4F5; color:#8C2F3C; border-radius:12px; }
</style>
</head>
<body>
<div class="card">
<h1>Recomendador de Looks</h1>
<form method="post">
<select name="indice">
{% for _, r in prendas.iterrows() %}
<option value="{{ r.indice }}" {% if r.indice == selected_indice %}selected{% endif %}>
{{ r.title }}
</option>
{% endfor %}
</select>
<br><br>
<button type="submit">Generar recomendación</button>
</form>

{% if look %}
<div class="result-box">
    <h2>Look recomendado</h2>
    <ul>
    <li><strong>Prenda Base:</strong> {{ look[0] }}</li>
    <li><strong>Complemento 1:</strong> {{ look[1] }}</li>
    <li><strong>Complemento 2:</strong> {{ look[2] }}</li>
    </ul>
</div>
{% endif %}

{% if no_combinaciones %}
<div class="warning">
La prenda seleccionada no dispone de suficientes combinaciones.
</div>
{% endif %}
</div>
</body>
</html>"""





def esperar_look(prenda_id, timeout=20):
    start = time.time()

    while time.time() - start < timeout:
        try:
            df = pd.read_csv(csv_path)
            df['item_objetivo'] = df['item_objetivo'].astype(int)
            df_f = df[df['item_objetivo'] == prenda_id]

            if not df_f.empty:
                return df_f.iloc[-1]

        except (pd.errors.ParserError, pd.errors.EmptyDataError):
            pass

        time.sleep(0.4)

    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    look = None
    no_combinaciones = False
    selected_indice = None

    if request.method == 'POST':
        selected_indice = int(request.form['indice'])

        producer.produce(
            TOPIC,
            json.dumps({
                "tipo": "SOLICITUD_PREDICCION",
                "item_objetivo": selected_indice
            }).encode('utf-8')
        )
        producer.flush()

        last = esperar_look(selected_indice)

        if last is not None:
            look = [last['Prenda Objetivo'], last['Vecino 1'], last['Vecino 2']]
        else:
            no_combinaciones = True

    return render_template_string(
        HTML,
        prendas=df_30,
        look=look,
        selected_indice=selected_indice,
        no_combinaciones=no_combinaciones
    )


if __name__ == '__main__':
    threading.Thread(target=consumer_loop, daemon=True).start()
    app.run(debug=True, use_reloader=False)
