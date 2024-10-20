from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Función para evaluar el contenido según los modelos pedagógicos
def evaluar_contenido(texto, palabras_clave_enseñanza, palabras_clave_indagacion):
    # Evaluar cuántas palabras clave del modelo aparecen en el texto del servicio educativo
    puntaje_enseñanza = sum([1 for palabra in palabras_clave_enseñanza if palabra in texto.lower()])
    puntaje_indagacion = sum([1 for palabra in palabras_clave_indagacion if palabra in texto.lower()])

    # Normalizar los puntajes (por ejemplo, de 1 a 5)
    puntaje_enseñanza = min(5, puntaje_enseñanza)
    puntaje_indagacion = min(5, puntaje_indagacion)

    # Devolver los puntajes y una observación
    if puntaje_enseñanza > 0 and puntaje_indagacion > 0:
        observacion = "Se mencionan conceptos clave de ambos modelos pedagógicos."
    elif puntaje_enseñanza > 0:
        observacion = "Se mencionan conceptos clave del modelo Enseñanza para la Comprensión."
    elif puntaje_indagacion > 0:
        observacion = "Se mencionan conceptos clave del modelo Indagación Científica."
    else:
        observacion = "No se mencionan conceptos clave en esta sección."

    return {
        "puntaje_enseñanza": puntaje_enseñanza,
        "puntaje_indagacion": puntaje_indagacion,
        "observacion": observacion
    }

# Endpoint para procesar el servicio educativo
@app.route('/procesar', methods=['POST'])
def procesar_servicio():
    datos_servicio = request.json

    # Obtener secciones del servicio educativo
    introduccion = datos_servicio.get('introduccion', '')
    objetivos = datos_servicio.get('objetivos', '')
    preconceptos = datos_servicio.get('preconceptos', '')
    implicaciones = datos_servicio.get('implicaciones', '')
    actividades = datos_servicio.get('actividades', '')

    # Palabras clave de los modelos pedagógicos
    palabras_clave_enseñanza = ["comprensión", "conocimiento", "problemas", "reflexión"]
    palabras_clave_indagacion = ["hipótesis", "observación", "investigación", "experimento"]

    # Evaluar cada sección
    evaluacion_introduccion = evaluar_contenido(introduccion, palabras_clave_enseñanza, palabras_clave_indagacion)
    evaluacion_objetivos = evaluar_contenido(objetivos, palabras_clave_enseñanza, palabras_clave_indagacion)
    evaluacion_preconceptos = evaluar_contenido(preconceptos, palabras_clave_enseñanza, palabras_clave_indagacion)
    evaluacion_implicaciones = evaluar_contenido(implicaciones, palabras_clave_enseñanza, palabras_clave_indagacion)
    evaluacion_actividades = evaluar_contenido(actividades, palabras_clave_enseñanza, palabras_clave_indagacion)

    # Resultado de ejemplo
    resultado = {
        "modelo_educativo": "Enseñanza para la Comprensión e Indagación Científica",
        "evaluacion": {
            "introduccion": evaluacion_introduccion,
            "objetivos": evaluacion_objetivos,
            "preconceptos": evaluacion_preconceptos,
            "implicaciones": evaluacion_implicaciones,
            "actividades": evaluacion_actividades
        },
        "observacion_general": "Evaluación basada en palabras clave de los modelos pedagógicos."
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)

