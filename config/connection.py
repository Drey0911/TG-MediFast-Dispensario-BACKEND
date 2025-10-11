import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()

db = SQLAlchemy()

def get_db_connection(app):
    database_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'poolclass': NullPool, 
    }
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            db.session.remove() 
            print("Conexión a BD establecida correctamente (NullPool)")
        except Exception as e:
            print(f"Error conectando a BD: {e}")
    
    return db