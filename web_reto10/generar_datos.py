import joblib
import pandas as pd
import json
import os
import random

def generar_datos_web():
    print("--- INICIANDO EXPORTACIÓN DE DATOS ---")
    
    # 1. Cargar archivos originales
    print("1. Cargando grafo y CSV...")
    try:
        G = joblib.load('grafo_season9.pkl')
        df = pd.read_csv('season9_limpios.csv')
    except FileNotFoundError:
        print("ERROR: No se encuentran 'grafo_season9.pkl' o 'season9_limpios.csv'.")
        return

    # 2. Procesar Nodos (Prendas)
    print("2. Procesando prendas...")
    nodes_data = {}
    
    for _, row in df.iterrows():
        idx = int(row['indice'])
        title = str(row['title'])
        # Extraemos una categoría simple del título
        parts = title.split()
        tipo = parts[1] if len(parts) > 1 else parts[0]
        
        nodes_data[idx] = {
            "title": title,
            "type": tipo
        }

    # 3. Procesar Conexiones (Grafo)
    print("3. Exportando conexiones...")
    graph_edges = {}
    valid_ids = []

    for node in G.nodes():
        if node in nodes_data:
            neighbors = []
            if node in G:
                # Convertir vecinos a lista simple con pesos
                for neighbor, attrs in G[node].items():
                    if neighbor in nodes_data:
                        neighbors.append({
                            "id": int(neighbor),
                            "weight": attrs.get('weight', 1.0)
                        })
            
            # Ordenar por peso (mejores combinaciones primero)
            neighbors.sort(key=lambda x: x['weight'], reverse=True)
            
            # Solo guardamos si tiene suficientes conexiones para hacer un outfit
            if len(neighbors) >= 2:
                graph_edges[int(node)] = neighbors
                valid_ids.append(int(node))

    # 4. Seleccionar muestra para el menú (máximo 50 para no saturar)
    print("4. Creando lista de selección...")
    random.seed(42)
    display_ids = random.sample(valid_ids, min(50, len(valid_ids)))

    full_data = {
        "nodes": nodes_data,
        "edges": graph_edges,
        "display_ids": display_ids
    }

    # 5. Guardar archivo JS
    carpeta = 'scripts'
    archivo = 'datos_graph.js'
    ruta = os.path.join(carpeta, archivo)

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    with open(ruta, 'w', encoding='utf-8') as f:
        json_str = json.dumps(full_data, ensure_ascii=False)
        f.write(f"const GRAPH_DATA = {json_str};")

    print(f"\n¡LISTO! Archivo creado en: {ruta}")

if __name__ == "__main__":
    generar_datos_web()