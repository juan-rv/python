import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [introduccion, setIntroduccion] = useState('');
  const [objetivos, setObjetivos] = useState('');
  const [preconceptos, setPreconceptos] = useState('');
  const [implicaciones, setImplicaciones] = useState('');
  const [actividades, setActividades] = useState('');
  const [resultado, setResultado] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const servicioEducativo = {
      introduccion,
      objetivos,
      preconceptos,
      implicaciones,
      actividades
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/procesar', servicioEducativo, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setResultado(response.data);
      
      // Borrar los campos de entrada después de enviar
      setIntroduccion('');
      setObjetivos('');
      setPreconceptos('');
      setImplicaciones('');
      setActividades('');
    } catch (error) {
      console.error('Error al procesar el servicio educativo:', error);
    }
  };

  return (
    <div>
      <h1>Evaluación de Servicio Educativo</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Introducción:</label>
          <textarea 
            value={introduccion} 
            onChange={(e) => setIntroduccion(e.target.value)} 
            placeholder="Escribe la introducción aquí"
          />
        </div>
        <div>
          <label>Objetivos:</label>
          <textarea 
            value={objetivos} 
            onChange={(e) => setObjetivos(e.target.value)} 
            placeholder="Escribe los objetivos aquí"
          />
        </div>
        <div>
          <label>Preconceptos:</label>
          <textarea 
            value={preconceptos} 
            onChange={(e) => setPreconceptos(e.target.value)} 
            placeholder="Escribe los preconceptos aquí"
          />
        </div>
        <div>
          <label>Implicaciones Conceptuales:</label>
          <textarea 
            value={implicaciones} 
            onChange={(e) => setImplicaciones(e.target.value)} 
            placeholder="Escribe las implicaciones conceptuales aquí"
          />
        </div>
        <div>
          <label>Actividades:</label>
          <textarea 
            value={actividades} 
            onChange={(e) => setActividades(e.target.value)} 
            placeholder="Escribe las actividades aquí"
          />
        </div>
        <button type="submit">Evaluar</button>
      </form>

      {resultado && (
        <div>
          <h2>Resultado de la Evaluación:</h2>
          <pre>{JSON.stringify(resultado, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;