import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env.
# load_dotenv no sobrescribirá las variables que ya están establecidas en el entorno,
# por lo que las variables de Render tendrán prioridad.
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
database_url = os.environ.get('DATABASE_URL')
# Si DATABASE_URL existe (en Render), úsala. De lo contrario (local), usa SQLite.
# Esto funciona para URLs que empiezan con 'postgres://' y 'postgresql://'.
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("postgres://", "postgresql://", 1)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Verifica conexiones antes de usarlas
    'pool_recycle': 300,    # Recicla conexiones cada 5 minutos
}
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# ✅ Configuración de correo
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASS'),
    "MAIL_DEFAULT_SENDER": os.environ.get('EMAIL_USER')
}
app.config.update(mail_settings)

mail = Mail(app)

from taskapp import routes

# Es mejor crear un comando para inicializar la base de datos
# en lugar de llamarlo cada vez que se inicia la aplicación.
# Puedes ejecutar esto desde tu terminal con: flask init-db
@app.cli.command('init-db')
def init_db_command():
    """Crea las tablas de la base de datos."""
    db.create_all()
    print('Base de datos inicializada.')