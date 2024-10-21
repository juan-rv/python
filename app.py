from flask import Flask, request, jsonify
from difflib import SequenceMatcher
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS correctamente

# Verificar si el archivo de modelos pedagógicos existe
data_path = 'data/modelos_pedagogicos.json'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"El archivo {data_path} no se encuentra.")

# Cargar el archivo JSON con la información de los modelos pedagógicos
with open(data_path, 'r') as f:
    modelos_pedagogicos = json.load(f)

# Cargar el modelo y tokenizador de Hugging Face
modelo = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
tokenizador = AutoTokenizer.from_pretrained('distilbert-base-uncased')

# Función para medir similitud entre cadenas
def similitud(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Función para evaluar cada sección con respecto a ambos modelos pedagógicos
def evaluar_seccion(seccion_text, caracteristicas_epc, caracteristicas_indagacion):
    if isinstance(seccion_text, list):
        # Asegurarse de que todos los elementos sean cadenas antes de hacer join
        seccion_text = ' '.join([str(item) for item in seccion_text])
    
    puntaje_epc = 0
    puntaje_indagacion = 0
    resultados_epc = {}
    resultados_indagacion = {}

    # Evaluar con las características de Enseñanza para la Comprensión
    for clave, detalle in caracteristicas_epc.items():
        descripcion = detalle["descripcion"]
        puntaje = similitud(seccion_text.lower(), descripcion.lower())
        resultados_epc[clave] = {
            "observacion": f"Similitud con {clave}: {puntaje:.2f}",
            "evaluacion": round(puntaje * 5)
        }
        puntaje_epc += round(puntaje * 5)

    # Evaluar con las características de Indagación Científica
    for clave, detalle in caracteristicas_indagacion.items():
        descripcion = detalle["descripcion"]
        puntaje = similitud(seccion_text.lower(), descripcion.lower())
        resultados_indagacion[clave] = {
            "observacion": f"Similitud con {clave}: {puntaje:.2f}",
            "evaluacion": round(puntaje * 5)
        }
        puntaje_indagacion += round(puntaje * 5)

    return resultados_epc, resultados_indagacion

# Ruta principal para procesar el servicio educativo
@app.route('/procesar', methods=['POST'])
def procesar_servicio():
    datos_servicio = request.json
    if not datos_servicio:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    # Evaluar cada sección del servicio educativo con ambos modelos
    evaluacion_introduccion = evaluar_seccion(
        datos_servicio.get('introduccion', ''), 
        modelos_pedagogicos['epc']['caracteristicas'], 
        modelos_pedagogicos['indagacion']['caracteristicas']
    )
    evaluacion_objetivos = evaluar_seccion(
        datos_servicio.get('objetivos', ''), 
        modelos_pedagogicos['epc']['caracteristicas'], 
        modelos_pedagogicos['indagacion']['caracteristicas']
    )
    evaluacion_preconceptos = evaluar_seccion(
        datos_servicio.get('preconceptos', ''), 
        modelos_pedagogicos['epc']['caracteristicas'], 
        modelos_pedagogicos['indagacion']['caracteristicas']
    )
    evaluacion_implicaciones = evaluar_seccion(
        datos_servicio.get('implicaciones', ''), 
        modelos_pedagogicos['epc']['caracteristicas'], 
        modelos_pedagogicos['indagacion']['caracteristicas']
    )
    evaluacion_actividades = evaluar_seccion(
        datos_servicio.get('actividades', ''), 
        modelos_pedagogicos['epc']['caracteristicas'], 
        modelos_pedagogicos['indagacion']['caracteristicas']
    )

    resultado = {
        "modelo_educativo": "Enseñanza para la Comprensión e Indagación Científica",
        "evaluacion": {
            "introduccion": {
                "epc": evaluacion_introduccion[0],
                "indagacion": evaluacion_introduccion[1]
            },
            "objetivos": {
                "epc": evaluacion_objetivos[0],
                "indagacion": evaluacion_objetivos[1]
            },
            "preconceptos": {
                "epc": evaluacion_preconceptos[0],
                "indagacion": evaluacion_preconceptos[1]
            },
            "implicaciones": {
                "epc": evaluacion_implicaciones[0],
                "indagacion": evaluacion_implicaciones[1]
            },
            "actividades": {
                "epc": evaluacion_actividades[0],
                "indagacion": evaluacion_actividades[1]
            }
        },
        "observacion_general": "Evaluación basada en la comparación con las descripciones clave de los modelos pedagógicos."
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)