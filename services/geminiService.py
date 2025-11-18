import os
import requests
import json
from config.connection import db
from models.medModel import Medicamentos
from models.dispModel import Disponibilidad
from models.sedeModel import Sede
from datetime import datetime

class GeminiService:
    def __init__(self):
        # No defaults with secrets here: leer solo desde .env / entorno
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = os.getenv('GEMINI_API_URL')
        
        # Validar que las variables de entorno estén cargadas (no imprimir valores)
        if self.api_key and self.base_url:
            print("Variables de entorno GEMINI_API_KEY y GEMINI_API_URL cargadas.")
        else:
            print("ADVERTENCIA: No se encontraron GEMINI_API_KEY y/o GEMINI_API_URL. Asegúrate de cargar el archivo .env.")
    
    def get_medicamentos_disponibles(self):
        """Obtener medicamentos disponibles con su stock"""
        try:
            disponibilidades = db.session.query(Disponibilidad).join(Medicamentos).join(Sede).filter(
                Disponibilidad.stock > 0
            ).all()
            
            medicamentos_info = []
            for disp in disponibilidades:
                medicamento_info = {
                    'nombre': disp.medicamento.nombreMedicamento,
                    'tipo': disp.medicamento.tipo,
                    'descripcion': disp.medicamento.descripcion,
                    'sede': disp.sede.nombreSede,
                    'stock': disp.stock,
                    'estado': disp.estado
                }
                medicamentos_info.append(medicamento_info)
            
            return medicamentos_info
        except Exception as e:
            print(f"Error al obtener medicamentos disponibles: {e}")
            return []
    
    def get_medicamentos_por_tipo(self, tipo_busqueda):
        """Buscar medicamentos por tipo o condición"""
        try:
            # Buscar en nombre, tipo o descripción
            medicamentos = Medicamentos.query.filter(
                db.or_(
                    Medicamentos.nombreMedicamento.ilike(f'%{tipo_busqueda}%'),
                    Medicamentos.tipo.ilike(f'%{tipo_busqueda}%'),
                    Medicamentos.descripcion.ilike(f'%{tipo_busqueda}%')
                )
            ).all()
            
            # Verificar disponibilidad
            resultados = []
            for med in medicamentos:
                disponibilidades = Disponibilidad.query.filter_by(
                    id_medicamento=med.id, 
                    stock__gt=0
                ).join(Sede).all()
                
                if disponibilidades:
                    for disp in disponibilidades:
                        resultados.append({
                            'medicamento': med.nombreMedicamento,
                            'tipo': med.tipo,
                            'descripcion': med.descripcion,
                            'sede': disp.sede.nombreSede,
                            'stock': disp.stock,
                            'estado': disp.estado
                        })
            
            return resultados
        except Exception as e:
            print(f"Error al buscar medicamentos por tipo: {e}")
            return []
    
    def generar_respuesta_chatbot(self, mensaje_usuario):
        """Generar respuesta del chatbot usando Gemini AI API REST"""
        try:
            # Obtener información actual de medicamentos
            medicamentos_disponibles = self.get_medicamentos_disponibles()
            
            # Crear prompt contextualizado
            prompt = f"""
            Eres un asistente virtual de un dispensario médico. Tu función es ayudar a los usuarios a encontrar medicamentos disponibles basándote en sus síntomas o necesidades.

            INFORMACIÓN ACTUAL DEL DISPENSARIO:
            {json.dumps(medicamentos_disponibles, indent=2, ensure_ascii=False)}

            REGLAS IMPORTANTES:
            1. SOLO recomienda medicamentos que estén actualmente disponibles en el stock
            2. Si no hay medicamentos disponibles para una condición, sugiere alternativas pero DEJA CLARO que no están disponibles actualmente
            3. Sé preciso y profesional
            4. Incluye información sobre en qué sede está disponible y el stock actual cuando sea relevante
            5. Si el usuario pregunta por algo muy general como "dolor", pregunta por síntomas específicos
            6. Recuerda que no eres un médico, solo un asistente del dispensario
            7. Responde en español de manera clara y amable
            8. Si preguntan por disponibilidad específica, consulta la lista de medicamentos disponibles proporcionada
            9. **NO USES FORMATO MARKDOWN** (sin **asteriscos**, _guiones bajos_, o cualquier formato especial)
            10. Usa texto plano solamente
            11. Separa las ideas con saltos de línea normales
            12. Si preguntan por medicamentos en sedes especificas, toma la ubicacion que te dan, y responde solo con la informacion de esa sede especifica tomada de la base de datos por el nombreSede
            13. Si es informacion general puedes filtrar por sede pero no es obligatorio

            MENSAJE DEL USUARIO: {mensaje_usuario}

            Responde de manera útil y amable, enfocándote en lo que realmente está disponible.
            """
            
            # Preparar la solicitud a la API de Gemini
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.api_key
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            # Hacer la solicitud a la API
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                respuesta_texto = response_data['candidates'][0]['content']['parts'][0]['text']
                
                return {
                    'respuesta': respuesta_texto,
                    'medicamentos_relevantes': self._extraer_medicamentos_relevantes(respuesta_texto, medicamentos_disponibles),
                    'timestamp': datetime.now()
                }
            else:
                print(f"Error en API Gemini: {response.status_code} - {response.text}")
                return {
                    'respuesta': "Lo siento, estoy teniendo dificultades técnicas. Por favor, intenta nuevamente en unos momentos.",
                    'medicamentos_relevantes': [],
                    'timestamp': datetime.now()
                }
            
        except Exception as e:
            print(f"Error en chatbot: {e}")
            return {
                'respuesta': "Lo siento, estoy teniendo dificultades para acceder a la información. Por favor, intenta nuevamente.",
                'medicamentos_relevantes': [],
                'timestamp': datetime.now()
            }
    
    def _extraer_medicamentos_relevantes(self, respuesta, medicamentos_disponibles):
        """Extraer medicamentos mencionados en la respuesta"""
        medicamentos_mencionados = []
        for med in medicamentos_disponibles:
            if med['nombre'].lower() in respuesta.lower():
                medicamentos_mencionados.append(med)
        return medicamentos_mencionados

# Instancia global del servicio
gemini_service = GeminiService()