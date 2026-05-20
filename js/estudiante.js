// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificar sesión del estudiante
    const estudianteId = localStorage.getItem('estudiante_id');
    const estudianteNombre = localStorage.getItem('estudiante_nombre');

    if (!estudianteId) {
        alert('Sesión no válida. Por favor, inicia sesión.');
        window.location.href = '../../index.html';
        return;
    }

    // Mostrar el nombre del estudiante en el perfil
    document.getElementById('student-name-display').innerText = estudianteNombre;

    // 2. Cargar lista de productores (Chinampas)
    cargarProductores();

    // 3. Cargar historial de monitoreos
    cargarHistorialMonitoreos(estudianteId);

    // 4. Manejo del formulario de registro
    const formMonitoreo = document.getElementById('form-registrar-monitoreo');
    if (formMonitoreo) {
        formMonitoreo.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(formMonitoreo);
            const data = Object.fromEntries(formData.entries());
            
            // Adjuntar el ID del estudiante
            data.id_estudiante = estudianteId;

            try {
                const response = await fetch(`${API_BASE_URL}/api/monitoreo`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Monitoreo registrado con éxito.');
                    formMonitoreo.reset();
                    // Recargar el historial
                    cargarHistorialMonitoreos(estudianteId);
                } else {
                    alert('Error al registrar monitoreo: ' + (result.error || 'Intente nuevamente.'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al conectar con el servidor.');
            }
        });
    }
});

// Función para cargar los productores en el dropdown select
async function cargarProductores() {
    const selectProductor = document.getElementById('select-productor');
    if (!selectProductor) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/productores`);
        const productores = await response.json();

        if (response.ok) {
            // Limpiar opciones anteriores pero mantener el placeholder
            selectProductor.innerHTML = '<option value="" disabled selected>Seleccione productor...</option>';
            productores.forEach(prod => {
                const opt = document.createElement('option');
                opt.value = prod.Id_Productor;
                opt.textContent = prod.Nombre;
                selectProductor.appendChild(opt);
            });
        } else {
            console.error('Error al obtener productores:', productores.error);
        }
    } catch (error) {
        console.error('Error de red al cargar productores:', error);
    }
}

// Función para cargar los monitoreos hechos por el estudiante
async function cargarHistorialMonitoreos(estudianteId) {
    const tbody = document.getElementById('tbody-monitoreos');
    if (!tbody) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/estudiante/monitoreos?id_estudiante=${estudianteId}`);
        const monitoreos = await response.json();

        if (response.ok) {
            if (monitoreos.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">No has registrado mediciones aún.</td></tr>`;
                return;
            }

            tbody.innerHTML = '';
            monitoreos.forEach(mon => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${mon.Fecha}</td>
                    <td><strong>${mon.Nombre_Productor}</strong></td>
                    <td><span class="badge-student" style="background: rgba(255,159,67,0.1); color: #ff9f43; padding: 2px 6px; border-radius: 4px;">${mon.PH}</span></td>
                    <td>${mon.Salinidad}</td>
                    <td>${mon.Humedad}%</td>
                    <td>${mon.Temperatura}°C</td>
                    <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${mon.Observaciones}">${mon.Observaciones}</td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            console.error('Error al cargar monitoreos:', monitoreos.error);
        }
    } catch (error) {
        console.error('Error de red al cargar historial:', error);
    }
}

// Función para cerrar sesión
function cerrarSesionEstudiante() {
    localStorage.removeItem('estudiante_id');
    localStorage.removeItem('estudiante_nombre');
    window.location.href = '../../index.html';
}
