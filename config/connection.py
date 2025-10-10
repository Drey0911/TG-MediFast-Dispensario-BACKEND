import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def get_db_connection(app):
    database_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')
    
    # Configuración específica para MySQL y problemas de conexión
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 280,           # Menor que wait_timeout de MySQL
        'pool_pre_ping': True,         # verifica conexión antes de cada query
        'pool_timeout': 30,
        'pool_size': 5,
        'max_overflow': 10,
        'connect_args': {
            'connect_timeout': 30,     # Timeout para establecer conexión
        }
    }
    
    db.init_app(app)
    
    # Verificar conexión al inicializar
    with app.app_context():
        try:
            db.engine.connect()
            print("Conexión a BD establecida correctamente")
        except Exception as e:
            print(f"Error conectando a BD: {e}")
    
    return db