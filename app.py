from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import json
import os

app = Flask(__name__)
CORS(app)

# Verificar si el archivo de modelos pedagógicos existe
data_path = 'data/modelos_pedagogicos.json'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"El archivo {data_path} no se encuentra.")

# Cargar el archivo JSON con la información de los modelos pedagógicos
with open(data_path, 'r') as f:
    modelos_pedagogicos = json.load(f)

# Inicializar un pipeline de clasificación de texto usando un modelo preentrenado
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Función para generar observaciones y puntuaciones con IA
def evaluar_con_ia(texto, etiquetas):
    resultado = classifier(texto, candidate_labels=etiquetas)
    return resultado

# Función para procesar cada apartado (introducción, objetivos, etc.)
def evaluar_seccion_ia(seccion_text, caracteristicas_epc, caracteristicas_indagacion):
    etiquetas_epc = list(caracteristicas_epc.keys())
    etiquetas_indagacion = list(caracteristicas_indagacion.keys())

    # Clasificar la sección con respecto a las etiquetas de EpC
    epc_resultado = evaluar_con_ia(seccion_text, etiquetas_epc)
    indagacion_resultado = evaluar_con_ia(seccion_text, etiquetas_indagacion)

    return {
        "epc": {
            "resultado": epc_resultado,
            "observacion": "Evaluación basada en el análisis IA para EpC."
        },
        "indagacion": {
            "resultado": indagacion_resultado,
            "observacion": "Evaluación basada en el análisis IA para Indagación Científica."
        }
    }

# Ruta principal para procesar el servicio educativo
@app.route('/procesar', methods=['POST'])
def procesar_servicio():
    datos_servicio = request.json
    if not datos_servicio:
        return jsonify({"error": "No se enviaron datos"}), 400

    # Evaluar con IA cada apartado del servicio educativo
    evaluacion_introduccion = evaluar_seccion_ia(
        datos_servicio.get('introduccion', ''),
        modelos_pedagogicos['epc']['caracteristicas'],
        modelos_pedagogicos['indagacion']['caracteristicas']
    )
    evaluacion_objetivos = evaluar_seccion_ia(
        datos_servicio.get('objetivos', ''),
        modelos_pedagogicos['epc']['caracteristicas'],
        modelos_pedagogicos['indagacion']['caracteristicas']
    )

    resultado = {
        "modelo_educativo": "Enseñanza para la Comprensión e Indagación Científica",
        "evaluacion": {
            "introduccion": evaluacion_introduccion,
            "objetivos": evaluacion_objetivos
        },
        "observacion_general": "Evaluación realizada por IA con observaciones generadas automáticamente."
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)