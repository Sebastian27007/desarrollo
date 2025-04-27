from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('main', __name__)

# Base de datos simulada (con ID único)
reservas = []
id_counter = 1  # Variable para generar ID únicos para cada reserva

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/reserva', methods=['GET', 'POST'])
def reserva():
    global id_counter  # Hacemos que el contador sea global
    if request.method == 'POST':
        sala = request.form['sala']
        fecha = request.form['fecha']
        usuario = request.form['usuario']
        
        # Crear un diccionario para la nueva reserva con un ID único
        nueva_reserva = {'id': id_counter, 'sala': sala, 'fecha': fecha, 'usuario': usuario}
        reservas.append(nueva_reserva)
        
        # Incrementar el ID para la próxima reserva
        id_counter += 1

        return redirect(url_for('main.reservas_view'))

    return render_template('reserva.html')

@bp.route('/reservas', methods=['GET', 'POST'])
def reservas_view():
    if request.method == 'POST':
        # Editar una reserva existente
        id_reserva = int(request.form['id'])
        reserva = next((res for res in reservas if res['id'] == id_reserva), None)
        if reserva:
            reserva['sala'] = request.form['sala']
            reserva['fecha'] = request.form['fecha']
            reserva['usuario'] = request.form['usuario']
        
        return redirect(url_for('main.reservas_view'))

    return render_template('reservas.html', reservas=reservas)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_reserva(id):
    # Filtrar la reserva para eliminarla
    global reservas
    reservas = [reserva for reserva in reservas if reserva['id'] != id]
    return redirect(url_for('main.reservas_view'))
