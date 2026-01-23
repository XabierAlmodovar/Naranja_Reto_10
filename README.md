# Naranja Reto 10: Valoración de una Call Asiática sobre una Cartera de Acciones del Dow Jones
## Explicación general

En este reto, los equipos trabajan sobre una problemática planteada por Lookiero relacionada con la mejora de la experiencia de las clientas en su producto principal, la caja Lookiero, que contiene una selección personalizada de prendas. El proyecto se aborda desde la perspectiva del customer experience (CX), poniendo el foco en el cuestionario inicial de las usuarias y en el proceso de selección de prendas.

Para ello, se analiza la user experience (UX) de la plataforma a partir de datos simulados de uso web, utilizando herramientas como Google Analytics para extraer información relevante y facilitar la toma de decisiones. Asimismo, se desarrolla un sistema de generación de looks basado en grafos y modelos predictivos, junto con una interfaz de visualización interactiva, con el objetivo de apoyar el trabajo de las personal shoppers y mejorar la experiencia global de las clientas.

## Objetivos del reto

1. **Análisis de UX** .
2. **Generar looks en base a la teoría de grafos** .
3. **Predicción de relaciones entre prendas** .
4. **Adicional: caracterización y análisis de los datos de Look&Like** .

## Requisitos para ejecutar el proyecto

Para ejecutar correctamente el proyecto, es necesario crear un entorno Python con las librerías incluidas en el archivo "requirements.txt".
Ejemplo de instalación:
```pop install -r requirements.txt```
El proyecto **no incluye los datos originales** ni los datasets generados durante el proceso.
Se deben incorporar manualmente en una carpeta llamada "Datos/", siguiendo la estructura definida en el informe del reto (enviado por mudle en el apartado "Entrega final".

## Estructura del proyecto

| Archivo / Carpeta               | Descripción                                                                                                                              |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `.gitignore`                    | Oculta los archivos de datos (`.csv`) para no subirlos al repositorio.                                                     |
| `0-Limpieza_O2.ipynb`           | Notebook dedicado al **preprocesamiento y limpieza** de los datos originales del Dow Jones.                                              |
| `1-Montecarlo_Naranja.ipynb`    | Implementación de la **simulación Montecarlo** para generar datos sintéticos y modelar la evolución de los tres activos.                 |
| `1b-Formula_BBVA.ipynb`         | Definición de la fórmula matemática del activo BBVA, aplicando los parámetros necesarios para calcular su evolución y valor dentro de la cartera    |
| `2-Calculos_financieros.ipynb`  | Cálculo del **payoff**, **valor presente (prima)** y comparativa de resultados teóricos.                                                  |
| `3-Data_Science.ipynb`            | Contiene el desarrollo del **análisis de las series temporales** de las tres acciones que forman la cartera.                             |
| `4-Hiperparametros.ipynb`         | Notebook donde se experimenta con los **hiperparámetros** del modelo (número de capas, tasa de aprendizaje, épocas, etc.).               |
| `1c-Red_Neuronal.ipynb`            | Construcción, entrenamiento y evaluación una red neuronal LSTM, para analizar el rendimiento y comparar distintas configuraciones del modelo        |
| `funciones.py`                  | Archivo auxiliar con **funciones personalizadas** utilizadas en distintos notebooks (por ejemplo, para cálculos financieros o métricas). |
| `requirements.txt`              | Contiene las **librerías necesarias** para la ejecución del proyecto.                                                                    |
| `README.md`                     | Documento actual que explica la **estructura y funcionamiento** del proyecto.

## Orden de Ejecución de los Notebooks

1. `0-Limpieza_O2.ipynb` → Limpieza y preparación de los datos originales.
2. `1-Montecarlo_Naranja.ipynb` → Simulación de precios mediante el método de Montecarlo.
3. `1b-Formula_BBVA.ipynb` → Definición de la fórmula del activo BBVA.
4. `2-Calculos_financieros.ipynb`→ Cálculo del payoff, prima y comparaciones.
5. `3-Data_Science.ipynb` → Análisis de las series temporales.
6. `4-Hiperparametros.ipynb` → Ajuste de parámetros y análisis de rendimiento.
7. `1c-Red_Neuronal.ipynb`→ Construcción, entrenamiento y evaluación de una LSTM.

## Tecnologías y librerías utilizadas

- Python
- NumPy, Pandas, SciPy, Matplotlib
- scikit-learn, TensorFlow (para redes neuronales)
- Jupyter Notebook

## Conclusión

El proyecto combina **finanzas cuantitativas** y **machine learning** para abordar un problema clásico del sector financiero: la valoración de derivados exóticos sin fórmula cerrada.
A través del método de Montecarlo y las técnicas de aprendizaje automático, se busca **mejorar la eficiencia y precisión** en la estimación del precio de una opción asiática sobre una cartera de acciones reales.
