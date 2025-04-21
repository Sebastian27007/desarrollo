document.addEventListener("DOMContentLoaded", function () {
    const loginScreen = document.getElementById('loginScreen');
    const mainScreen = document.getElementById('mainScreen');
    const loginBtn = document.getElementById('loginBtn');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('loginError');

    const manageRoomsBtn = document.getElementById('manageRoomsBtn');
    const manageReservationsBtn = document.getElementById('manageReservationsBtn');
    const viewProfileBtn = document.getElementById('viewProfileBtn');
    const viewNotificationsBtn = document.getElementById('viewNotificationsBtn');
    const manageEventsBtn = document.getElementById('manageEventsBtn');
    const adminDashboardBtn = document.getElementById('adminDashboardBtn');
    const contentSection = document.getElementById('contentSection');

    const rooms = [
        {name: 'Sala 1', id: 'room1', capacity: 10},
        {name: 'Sala 2', id: 'room2', capacity: 5},
        {name: 'Sala 3', id: 'room3', capacity: 20},
        {name: 'Sala 4', id: 'room4', capacity: 15}
    ];

    // Simulando las credenciales
    const validUsername = 'admin';
    const validPassword = '1234';

    // Login
    loginBtn.addEventListener('click', function () {
        const username = usernameInput.value;
        const password = passwordInput.value;

        if (username === validUsername && password === validPassword) {
            loginScreen.style.display = 'none';
            mainScreen.style.display = 'block';
        } else {
            loginError.style.display = 'block';
        }
    });

    // Mostrar el contenido dinámico de acuerdo a la selección
    function showContent(contentType) {
        contentSection.innerHTML = '';  // Limpiar la sección actual

        if (contentType === 'rooms') {
            showRoomSelection();
        } else if (contentType === 'reservations') {
            showReservations();
        } else if (contentType === 'profile') {
            showUserProfile();
        } else if (contentType === 'notifications') {
            showNotifications();
        } else if (contentType === 'events') {
            showEvents();
        } else if (contentType === 'dashboard') {
            showAdminDashboard();
        }
    }

    // Mostrar la selección de salas (con información falsa)
    function showRoomSelection() {
        contentSection.innerHTML = `<h3>Selección de Salas</h3>`;

        rooms.forEach(room => {
            const roomButton = document.createElement('button');
            roomButton.textContent = `${room.name} (Capacidad: ${room.capacity})`;
            roomButton.addEventListener('click', () => selectRoom(room));
            contentSection.appendChild(roomButton);
        });
    }

    // Seleccionar una sala y simular una reserva
    function selectRoom(room) {
        const reservationForm = document.createElement('div');
        reservationForm.innerHTML = `
            <h4>Reserva para: ${room.name}</h4>
            <label for="reservationDate">Fecha y hora de la reserva:</label>
            <input type="datetime-local" id="reservationDate">
            <button id="submitReservationBtn">Confirmar Reserva</button>
            <button id="cancelReservationBtn">Cancelar</button>
        `;
        contentSection.innerHTML = '';  // Limpiar la sección
        contentSection.appendChild(reservationForm);

        document.getElementById('submitReservationBtn').addEventListener('click', function () {
            const reserva = {
                nombre: prompt("Ingrese su nombre:"),
                espacio: room.name,
                fecha: document.getElementById('reservationDate').value
            };

            const reservaDiv = document.createElement('div');
            reservaDiv.textContent = `${reserva.nombre} ha reservado ${reserva.espacio} para el ${new Date(reserva.fecha).toLocaleString()}`;
            contentSection.appendChild(reservaDiv);

            alert("Reserva confirmada!");
        });

        document.getElementById('cancelReservationBtn').addEventListener('click', function () {
            showRoomSelection();  // Volver a la selección de salas
        });
    }

    // Mostrar las reservas simuladas
    function showReservations() {
        const reservations = [
            {nombre: 'Juan Pérez', sala: 'Sala 1', fecha: '2023-04-22T10:00'},
            {nombre: 'Ana Gómez', sala: 'Sala 2', fecha: '2023-04-22T12:00'},
            {nombre: 'Luis Martínez', sala: 'Sala 3', fecha: '2023-04-23T14:00'}
        ];

        contentSection.innerHTML = '<h3>Reservas Confirmadas</h3>';

        reservations.forEach(reservation => {
            const reservationDiv = document.createElement('div');
            reservationDiv.textContent = `${reservation.nombre} ha reservado ${reservation.sala} para el ${new Date(reservation.fecha).toLocaleString()}`;
            contentSection.appendChild(reservationDiv);
        });
    }

    // Mostrar el perfil de usuario simulado
    function showUserProfile() {
        contentSection.innerHTML = `<h3>Perfil de Usuario</h3>
            <p><strong>Nombre:</strong> Admin</p>
            <p><strong>Email:</strong> admin@example.com</p>
            <p><strong>Rol:</strong> Administrador</p>`;
    }

    // Mostrar las notificaciones simuladas
    function showNotifications() {
        const notifications = [
            {message: 'Tu reserva para la Sala 1 ha sido confirmada.'},
            {message: 'La Sala 2 está ocupada en la fecha que solicitaste.'},
            {message: 'Tu perfil ha sido actualizado correctamente.'}
        ];

        contentSection.innerHTML = '<h3>Notificaciones</h3>';

        notifications.forEach(notification => {
            const notificationDiv = document.createElement('div');
            notificationDiv.textContent = notification.message;
            contentSection.appendChild(notificationDiv);
        });
    }

    // Mostrar los eventos simulados
    function showEvents() {
        const events = [
            {name: 'Conferencia de Tecnología', date: '2023-05-10T09:00'},
            {name: 'Seminario de Marketing', date: '2023-06-15T14:00'}
        ];

        contentSection.innerHTML = '<h3>Eventos Especiales</h3>';

        events.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.textContent = `${event.name} - ${new Date(event.date).toLocaleString()}`;
            contentSection.appendChild(eventDiv);
        });
    }

    // Mostrar el Dashboard de administración simulado
    function showAdminDashboard() {
        contentSection.innerHTML = `<h3>Dashboard de Administración</h3>
            <p><strong>Total de Reservas:</strong> 15</p>
            <p><strong>Total de Eventos:</strong> 2</p>
            <p><strong>Total de Usuarios:</strong> 5</p>`;
    }

    // Funcionalidades adicionales
    manageRoomsBtn.addEventListener('click', function () {
        showContent('rooms');
    });

    manageReservationsBtn.addEventListener('click', function () {
        showContent('reservations');
    });

    viewProfileBtn.addEventListener('click', function () {
        showContent('profile');
    });

    viewNotificationsBtn.addEventListener('click', function () {
        showContent('notifications');
    });

    manageEventsBtn.addEventListener('click', function () {
        showContent('events');
    });

    adminDashboardBtn.addEventListener('click', function () {
        showContent('dashboard');
    });
});
