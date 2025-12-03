import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configuración de base de datos con fallback a SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url and (database_url.startswith('postgresql://') or database_url.startswith('postgres://')):
    # Render puede proporcionar 'postgres://', SQLAlchemy necesita 'postgresql://'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Si está configurada PostgreSQL, validar que no sea solo un placeholder
    if 'usuario:password' in database_url:
        # Es un placeholder, usar SQLite en su lugar
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    else:
        # URL de PostgreSQL válida
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Si no hay DATABASE_URL o no es PostgreSQL, usar SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///site.db'

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

from taskapp import routes, models

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()
