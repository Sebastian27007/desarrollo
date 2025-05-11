from flask import Flask
from flask_login import LoginManager
from supabase import create_client, Client

url = "https://bkqicjcoaocnksvhpmqn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrcWljamNvYW9jbmtzdmhwbXFuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY5MTg3MTIsImV4cCI6MjA2MjQ5NDcxMn0.bayFh1h0DSTaIUHpXnzkNnVd2rm_p6Qm8eo1zvEB2tc"
supabase: Client = create_client(url, key)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para sesiones
    
    # Configura Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Importante: Registrar el user_loader
    login_manager.user_loader(routes.load_user)
    
    return app