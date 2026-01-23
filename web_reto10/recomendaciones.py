import joblib
import pandas as pd
import json

# ===============================
# Cargar grafo
# ===============================
G = joblib.load("grafo_season9.pkl")

# ===============================
# Cargar CSV
# ===============================
df = pd.read_csv("season9_limpios.csv")

id_to_title = dict(zip(df["indice"], df["title"]))
id_to_color = dict(zip(df["indice"], df["color"]))

# ===============================
# Calcular vecinos más cercanos
# ===============================
recomendaciones = {}

for nodo in G.nodes:
    vecinos = sorted(
        G[nodo].items(),
        key=lambda x: x[1].get("weight", 1.0),
        reverse=True
    )[:2]

    if len(vecinos) < 2:
        continue

    recomendaciones[str(nodo)] = {
        "principal": {
            "title": id_to_title[nodo],
            "color": id_to_color[nodo]
        },
        "vecinos": [
            {
                "title": id_to_title[v[0]],
                "color": id_to_color[v[0]]
            }
            for v in vecinos
        ]
    }

# ===============================
# Guardar JSON
# ===============================
with open("recomendaciones.json", "w", encoding="utf-8") as f:
    json.dump(recomendaciones, f, ensure_ascii=False, indent=2)

print("✅ recomendaciones.json generado")
