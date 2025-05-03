from flask import Blueprint, render_template, request, redirect, url_for
import shelve

bp = Blueprint('main', __name__)

def obtener_reservas():
    with shelve.open('reservas.db') as db:
        return db.get('reservas', [])

def guardar_reservas(lista):
    with shelve.open('reservas.db') as db:
        db['reservas'] = lista

def get_next_id():
    with shelve.open('reservas.db') as db:
        id_actual = db.get('id_counter', 1)
        db['id_counter'] = id_actual + 1
        return id_actual

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        sala = request.form['sala']
        fecha = request.form['fecha']
        usuario = request.form['usuario']

        reservas = obtener_reservas()
        nueva_reserva = {
            'id': get_next_id(),
            'sala': sala,
            'fecha': fecha,
            'usuario': usuario
        }
        reservas.append(nueva_reserva)
        guardar_reservas(reservas)

        return redirect(url_for('main.reservas_view'))

    return render_template('reserva.html')

@bp.route('/reservas', methods=['GET', 'POST'])
def reservas_view():
    reservas = obtener_reservas()

    if request.method == 'POST':
        id_reserva = int(request.form['id'])
        for reserva in reservas:
            if reserva['id'] == id_reserva:
                reserva['sala'] = request.form['sala']
                reserva['fecha'] = request.form['fecha']
                reserva['usuario'] = request.form['usuario']
                break
        guardar_reservas(reservas)
        return redirect(url_for('main.reservas_view'))

    return render_template('reservas.html', reservas=reservas)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_reserva(id):
    reservas = obtener_reservas()
    reservas = [r for r in reservas if r['id'] != id]
    guardar_reservas(reservas)
    return redirect(url_for('main.reservas_view'))
