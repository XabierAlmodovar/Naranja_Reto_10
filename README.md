# Naranja Reto 10: Recomendador de prendas Lookiero basado en grafos
## Explicación general

En este reto, los equipos trabajan sobre una problemática planteada por Lookiero relacionada con la mejora de la experiencia de las clientas en su producto principal, la caja Lookiero, que contiene una selección personalizada de prendas. El proyecto se aborda desde la perspectiva del customer experience (CX), poniendo el foco en el cuestionario inicial de las usuarias y en el proceso de selección de prendas.

Para ello, se analiza la user experience (UX) de la plataforma a partir de datos simulados de uso web, utilizando herramientas como Google Analytics para extraer información relevante y facilitar la toma de decisiones. Asimismo, se desarrolla un sistema de generación de looks basado en grafos y modelos predictivos, junto con una interfaz de visualización interactiva, con el objetivo de apoyar el trabajo de las personal shoppers y mejorar la experiencia global de las clientas.

## Objetivos del reto

1. **Análisis de UX** .
2. **Generar looks en base a la teoría de grafos** .
3. **Predicción de relaciones entre prendas** .
4. **Adicional: caracterización y análisis de los datos de Look&Like** .

## Requisitos para ejecutar el proyecto

Para ejecutar correctamente el proyecto, este **incluye una carpeta de datos transformados** con un dataset resultados_combinaciones_actualizado.csv generado durante el proceso. En él se encuentran las combinaciones de colores empleadas como regla para el grafo. No se debe ejecutar el script de Scripts/app.py, donde se genera este .csv, ya que se han escogido los colores en base a las opciones escogidas por el grupo Naranja.

## Estructura del proyecto

| Archivo / Carpeta               | Descripción                                                                                                                              |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `.gitignore`                    | Oculta los archivos de datos (`.csv`) para no subirlos al repositorio.                                                     |
| `Scripts/01-Limpieza.ipynb`           | Notebook dedicado a la primera parte de la **limpieza** de los datos originales.                                              |
| `Scripts/02-Limpieza.ipynb`    | Notebook dedicado a la segunda parte de la **limpieza** de los datos originales.                 |
| `Scripts/03-Analisis Descriptivo.ipynb`    | Notebook dedicado al **análisis descriptivo** de los datos limpios y ya filtrados de las prendas.                 |
| `Scripts/04-Grafo y Red.ipynb`         | Script dedicado a la creación del grafo y la red neuronal     |
| `Scripts/05-UX Experience.ipynb`  | Cálculo del **payoff**, **valor presente (prima)** y comparativa de resultados teóricos.                                                  |
| `Scripts/app.py`  | Cálculo del **payoff**, **valor presente (prima)** y comparativa de resultados teóricos.                                                  |
| `Scripts/funciones.py`  | Archivo auxiliar con **funciones personalizadas** utilizadas en distintos notebooks (por ejemplo, para cálculos del grafo).                                                  |
| `Scripts/lookiero_colors.py`  | Aqui se incluye la paleta de colores principales y secundarios de Lookiero, para gráficos y demás.                                                  |
| `/bigdata`            | Esta subcarpeta contiene el desarrollo del entregable de BigData:**un pipeline de Kafka** con el que realizar recomendaciones de combinaciones de 3 prendas. El profesor deberá tener abierto docker y ejecutar docker compose up -d desde Powershell. Se ejecutará primero el producer.py, después el consumer.py, con los que se ejecutará el pipeline completo desde Python. Para una mayor personalización, se ha creado una app de Flask con la que escoger una prenda del grafo antes de realizar la misma arquitectura con Kafka, pero con una prenda escogida por el cliente. Para ello, se borrará primero look_generados.csv, creado anteriormente al ejecutar el consumer.py, y se ejecutará app.py para lanzar la aplicación Flask.                         |
| `/web_reto10`         | Carpeta donde se desarrolla el entregable de Visualización, una **web de visualización Lookiero**. En ella se incluyen archivos.html con datos de cada página, una carpeta /scripts donde están los .js, donde se realizan los gráficos pertinentes y otra carpeta /fotos, donde se incluyen las fotos que se muestran en la web. Para ejecutar la web se debe estar en la carpeta /web_reto10 y pulsar index.html para abrir la web.             |
| `1c-Red_Neuronal.ipynb`            | Construcción, entrenamiento y evaluación una red neuronal LSTM, para analizar el rendimiento y comparar distintas configuraciones del modelo        |
| `funciones.py`                  | Archivo auxiliar con **funciones personalizadas** utilizadas en distintos notebooks (por ejemplo, para cálculos del grafo). |
| `app.py`              | Es una app creada con Flask con la que se crearon las reglas de color del grafo, los integrantes del grupo eligieron que colores combinaban y cuales no entre los colores de Lookiero para después crear resultados_combinaciones.csv con las elecciones. Se crea                                                                     |
| `lookiero_colors.py`              | Paleta de colores de Lookiero.                                                                   |
| `README.md`                     | Documento actual que explica la **estructura y funcionamiento** del proyecto.

## Orden de Ejecución de los Notebooks

1. `01-Limpieza.ipynb`
2. `02-Limpieza.ipynb`
3. `03-Análisis Descriptivo.ipynb`
4. `04-Grafo y Red.ipynb'
5. `05-UX Experience.ipynb`
6. `funciones.py`
7. `lookiero_colors.py`
7. `3-Data_Science.ipynb` → Análisis de las series temporales.
8. `4-Hiperparametros.ipynb` → Ajuste de parámetros y análisis de rendimiento.
9. `1c-Red_Neuronal.ipynb`→ Construcción, entrenamiento y evaluación de una LSTM.

## Tecnologías y librerías utilizadas

- Python
- NumPy, Pandas, Flask, Matplotlib, Kafka, D3
- scikit-learn, joblib, torch, networkx (para grafos)
- Jupyter Notebook

## Conclusión

El análisis de datos de UX permite identificar puntos de mejora clave en el proceso de onboarding y en la experiencia de las clientas.
Por otro lado, el uso de grafos y modelos predictivos facilita la generación de recomendaciones de looks coherentes y escalables. En cuanto a la programación, la combinación de análisis de datos y visualizaciones interactivas mejora la toma de decisiones de las personal shoppers.Esto permite a Lookiero integrar técnicas de Big Data y Machine Learning para personalizar la experiencia de las clientas de forma más eficiente.


El uso de grafos y modelos predictivos facilita la generación de recomendaciones de looks coherentes y escalables.

La combinación de análisis de datos y visualizaciones interactivas mejora la toma de decisiones de las personal shoppers.

Integrar técnicas de Big Data y Machine Learning contribuye a personalizar la experiencia de las clientas de forma más eficiente.
