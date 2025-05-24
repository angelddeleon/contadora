from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from config import Config
from routes import main_routes
from models import db, Usuario
from functools import wraps
from werkzeug.security import generate_password_hash



# Inicializar la aplicación Flask
app = Flask(__name__)
application = app
app.config.from_object(Config)

# Inicializar la instancia de SQLAlchemy
db.init_app(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"  # Ruta a la que se redirige si no está autenticado

# Registrar las rutas desde otro archivo
app.register_blueprint(main_routes)

hashed_password = generate_password_hash("123456")

print("Contraseña hasheada:", hashed_password)



# Función de carga del usuario (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
