from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash

# Configura Supabase
url = "https://bkqicjcoaocnksvhpmqn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrcWljamNvYW9jbmtzdmhwbXFuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY5MTg3MTIsImV4cCI6MjA2MjQ5NDcxMn0.bayFh1h0DSTaIUHpXnzkNnVd2rm_p6Qm8eo1zvEB2tc" 
supabase: Client = create_client(url, key)

bp = Blueprint('main', __name__)

# Configura Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'main.dashboard'  # Redirigir a la página de dashboard si no está autenticado

login_manager.init_app(bp)

# Clase de usuario para Flask-Login
class User:
    def __init__(self, id, email):
        self.id = id
        self.email = email

# Cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    user_data = supabase.table('users').select('*').eq('id', user_id).execute()
    if user_data.data:
        user = type('User', (), {
            'id': user_data.data[0]['id'],
            'email': user_data.data[0]['email'],
            'is_authenticated': True,
            'is_active': True,
            'is_anonymous': False,
            'get_id': lambda: str(user_data.data[0]['id'])
        })
        return user
    return None

# Funciones para reservas
def obtener_reservas():
    response = supabase.table('reservas').select('*').execute()
    return response.data

def guardar_reservas(lista):
    for reserva in lista:
        supabase.table('reservas').upsert(reserva).execute()

def get_next_id():
    response = supabase.table('reservas').select('id').order('id', desc=True).limit(1).execute()
    if response.data:
        return response.data[0]['id'] + 1
    return 1

# Ruta principal unificada
@bp.route('/')
@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Manejar login
        if 'login-email' in request.form:
            email = request.form['login-email']
            password = request.form['login-password']
            
            user_data = supabase.table('users').select('*').eq('email', email).execute()
            
            if user_data.data and check_password_hash(user_data.data[0]['password'], password):
                user = load_user(user_data.data[0]['id'])
                login_user(user)
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Credenciales inválidas', 'danger')
                return redirect(url_for('main.dashboard'))
        
        # Manejar registro
        elif 'register-email' in request.form:
            email = request.form['register-email']
            password = request.form['register-password']
            
            existing_user = supabase.table('users').select('*').eq('email', email).execute()
            
            if existing_user.data:
                flash('El correo ya está registrado', 'danger')
            else:
                hashed_password = generate_password_hash(password)
                new_user = supabase.table('users').insert({
                    'email': email,
                    'password': hashed_password
                }).execute()
                
                if new_user.data:
                    flash('Registro exitoso. Por favor inicia sesión.', 'success')
                else:
                    flash('Error al registrar usuario', 'danger')
            
            return redirect(url_for('main.dashboard'))
    
    return render_template('dashboard.html')

# Resto de las rutas (sin cambios)
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.dashboard'))

@bp.route('/reserva', methods=['GET', 'POST'])
@login_required
def reserva():
    if request.method == 'POST':
        sala = request.form['sala']
        fecha = request.form['fecha']
        usuario = current_user.email

        reservas = obtener_reservas()
        nueva_reserva = {
            'id': get_next_id(),
            'sala': sala,
            'fecha': fecha,
            'usuario': usuario
        }
        reservas.append(nueva_reserva)
        guardar_reservas(reservas)
        flash('Reserva creada exitosamente', 'success')
        return redirect(url_for('main.reservas_view'))

    return render_template('reserva.html')

@bp.route('/reservas')
@login_required
def reservas_view():
    reservas = obtener_reservas()
    return render_template('reservas.html', reservas=reservas)

@bp.route('/eliminar/<int:id>')
@login_required
def eliminar_reserva(id):
    reservas = obtener_reservas()
    reservas = [r for r in reservas if r['id'] != id]
    guardar_reservas(reservas)
    flash('Reserva eliminada', 'success')
    return redirect(url_for('main.reservas_view'))
