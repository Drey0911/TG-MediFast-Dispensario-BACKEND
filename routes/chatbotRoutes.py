from flask import Blueprint, request, jsonify, current_app
from services.geminiService import gemini_service
from services.userService import UserService
from functools import wraps
from sqlalchemy.exc import OperationalError

chatbot_routes = Blueprint('chatbot_routes', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] if len(request.headers['Authorization'].split(" ")) > 1 else None
        
        if not token:
            return jsonify({'error': 'Su sesión expiró, inicie sesión de nuevo'}), 401
        
        user_data, error = UserService.verify_jwt(token)
        if error:
            return jsonify({'error': error}), 401
        
        request.current_user = user_data
        return f(*args, **kwargs)
    
    return decorated

@chatbot_routes.route('/chatbot/mensaje', methods=['POST'])
@token_required
def enviar_mensaje_chatbot():
    """Enviar mensaje al chatbot y obtener respuesta"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        mensaje = data.get('mensaje')
        if not mensaje:
            return jsonify({'error': 'El mensaje es requerido'}), 400
        
        # Generar respuesta usando Gemini
        respuesta = gemini_service.generar_respuesta_chatbot(mensaje)
        
        return jsonify({
            'respuesta': respuesta['respuesta'],
            'medicamentos_relevantes': respuesta['medicamentos_relevantes'],
            'timestamp': respuesta['timestamp'].isoformat() if respuesta['timestamp'] else None
        }), 200
        
    except OperationalError as e:
        print(f"Error de conexión a BD en chatbot: {e}")
        return jsonify({
            'error': 'Problema de conexión inestable. Intente nuevamente.'
        }), 503
    
    except Exception as e:
        print(f"Error en chatbot: {e}")
        return jsonify({'error': 'El servidor tardó mucho en responder, inténtelo de nuevo más tarde'}), 500

@chatbot_routes.route('/chatbot/medicamentos-disponibles', methods=['GET'])
@token_required
def get_medicamentos_disponibles():
    """Obtener lista de medicamentos disponibles para el chatbot"""
    try:
        medicamentos = gemini_service.get_medicamentos_disponibles()
        return jsonify(medicamentos), 200
        
    except Exception as e:
        print(f"Error al obtener medicamentos disponibles: {e}")
        return jsonify({'error': 'Error al obtener medicamentos disponibles'}), 500