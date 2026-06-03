// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('productor_dashboard.html')) {
        cargarDatosDashboard();
    }
});

async function cargarDatosDashboard() {
    // Fallback para recuperar sesión de los parámetros URL en modo file:// (cuando el localStorage está particionado por directorio)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('productor_id')) {
        localStorage.setItem('productor_id', urlParams.get('productor_id'));
    }
    if (urlParams.has('productor_nombre')) {
        localStorage.setItem('productor_nombre', urlParams.get('productor_nombre'));
    }
    
    const nombreProductor = localStorage.getItem('productor_nombre');
    const nameDisplay = document.getElementById('productor-name-display');
    if (nombreProductor && nameDisplay) {
        nameDisplay.innerText = nombreProductor;
    }

    const idProductor = localStorage.getItem('productor_id');
    
    if (!idProductor) {
        console.error('No se encontró ID de productor en sesión.');
        return;
    }

    try {
        // 1. Cargar Stats (Cuadros superiores)
        const responseStats = await fetch(`${API_BASE_URL}/api/productor/stats?id_productor=${idProductor}`);
        if (responseStats.ok) {
            const stats = await responseStats.json();
            renderizarStats(stats);
        }

        // 2. Cargar Notificaciones Recientes
        const responseNotifs = await fetch(`${API_BASE_URL}/api/productor/notificaciones?id_productor=${idProductor}`);
        if (responseNotifs.ok) {
            const notificaciones = await responseNotifs.json();
            renderizarNotificaciones(notificaciones);
        }

        // 3. Cargar Inventario de Cosechas
        const responseInventario = await fetch(`${API_BASE_URL}/api/productor/inventario?id_productor=${idProductor}`);
        if (responseInventario.ok) {
            const data = await responseInventario.json();
            renderizarInventarioCosechas(data.items || []);
        }

        // 4. Cargar Monitoreos Estudiantiles (para la alerta y tabla inferior)
        const responseMonitoreos = await fetch(`${API_BASE_URL}/api/productor/monitoreos?id_productor=${idProductor}`);
        if (responseMonitoreos.ok) {
            const monitoreos = await responseMonitoreos.json();
            renderizarMonitoreosEstudiantes(monitoreos);
        }
        
    } catch (error) {
        console.error('Error al cargar datos del dashboard:', error);
    }
}

function renderizarStats(stats) {
    const statValues = document.querySelectorAll('.stat-value');
    if (statValues.length >= 3) {
        statValues[0].innerText = stats.terreno_total;
        statValues[1].innerText = stats.cosechas_activas;
        statValues[2].innerText = `$${(stats.valor_neto / 1000).toFixed(1)}K`;
    }
}

function renderizarNotificaciones(notificaciones) {
    const tbody = document.querySelector('#table-notificaciones tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (notificaciones.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; color: var(--text-muted);">No hay notificaciones recientes.</td></tr>';
        return;
    }

    notificaciones.forEach(notif => {
        const tr = document.createElement('tr');
        
        let badgeTipo = '';
        let detalle = '';
        
        if (notif.Tipo === 'monitoreo') {
            badgeTipo = '<span class="status-badge status-active" style="background-color: var(--accent-orange); color: #fff;">Monitoreo</span>';
            detalle = `El estudiante <strong>${notif.Nombre_Estudiante}</strong> registró un monitoreo: pH <strong>${notif.PH}</strong>, Salinidad <strong>${notif.Salinidad} dS/m</strong>, Humedad <strong>${notif.Humedad}%</strong>, Temp. <strong>${notif.Temperatura}°C</strong>.`;
        } else if (notif.Tipo === 'compra') {
            badgeTipo = '<span class="status-badge status-active" style="background-color: var(--accent-green); color: #fff;">Compra</span>';
            detalle = `El cliente <strong>${notif.Nombre_Cliente}</strong> compró <strong>${notif.Cantidad} kg</strong> de <strong>${notif.Producto}</strong>. Total: <strong style="color: var(--accent-green); font-weight: bold;">$${notif.Total.toFixed(2)} MXN</strong>.`;
        }
        
        tr.innerHTML = `
            <td style="white-space: nowrap;">${formatearFechaHora(notif.Fecha)}</td>
            <td>${badgeTipo}</td>
            <td style="text-align: left;">${detalle}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderizarInventarioCosechas(items) {
    const tbody = document.querySelector('#table-inventario-cosechas tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color: var(--text-muted);">No hay cosechas en el inventario.</td></tr>';
        return;
    }

    items.forEach(item => {
        const tr = document.createElement('tr');
        
        let badgeEstado = '';
        if (item.Estado === 'Publicado') {
            badgeEstado = '<span class="status-badge status-active">Publicado</span>';
        } else if (item.Estado === 'En Bodega') {
            badgeEstado = '<span class="status-badge status-finished" style="background-color: #6c757d;">En Bodega</span>';
        } else if (item.Estado === 'Agotado') {
            badgeEstado = '<span class="status-badge status-finished" style="background-color: #dc3545;">Agotado</span>';
        } else {
            badgeEstado = `<span class="status-badge status-finished">${item.Estado}</span>`;
        }
        
        tr.innerHTML = `
            <td><strong>${item.Lote}</strong></td>
            <td>${item.Cantidad}</td>
            <td>${item.Unidad_Medida || 'Kg'}</td>
            <td style="color: var(--accent-green); font-weight: bold;">$${item.Precio_Actual.toFixed(2)} MXN</td>
            <td>${badgeEstado}</td>
        `;
        tbody.appendChild(tr);
    });
}

function formatearFechaHora(fechaStr) {
    if (!fechaStr) return 'N/A';
    const date = new Date(fechaStr);
    if (isNaN(date.getTime())) return fechaStr;
    return date.toLocaleString('es-MX', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function renderizarMonitoreosEstudiantes(monitoreos) {
    const table = document.getElementById('table-monitoreo-estudiantes');
    const alertaBox = document.getElementById('alerta-monitoreo-reciente');
    
    // Configurar banner de alerta si existe en el DOM
    if (alertaBox) {
        if (monitoreos && monitoreos.length > 0) {
            const ultimoMon = monitoreos[0];
            // Formatear fecha
            let fechaFormato = ultimoMon.Fecha;
            try {
                const d = new Date(ultimoMon.Fecha);
                if (!isNaN(d.getTime())) {
                    fechaFormato = d.toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' });
                }
            } catch(e) {}

            const desc = `El estudiante <strong>${ultimoMon.Nombre_Estudiante}</strong> registró una medición el <strong>${fechaFormato}</strong>: pH <strong>${ultimoMon.PH}</strong>, Salinidad <strong>${ultimoMon.Salinidad} dS/m</strong>, Humedad <strong>${ultimoMon.Humedad}%</strong> y Temp. <strong>${ultimoMon.Temperatura}°C</strong>.`;
            document.getElementById('alerta-monitoreo-detalles').innerHTML = desc;
            alertaBox.style.display = 'flex';
        } else {
            alertaBox.style.display = 'none';
        }
    }

    if (!table) return;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (!monitoreos || monitoreos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color: var(--text-muted);">No hay reportes de estudiantes registrados para tu chinampa.</td></tr>';
        return;
    }

    monitoreos.forEach(mon => {
        // Formatear la fecha para la tabla
        let fechaCelda = mon.Fecha;
        try {
            const d = new Date(mon.Fecha);
            if (!isNaN(d.getTime())) {
                fechaCelda = d.toLocaleDateString('es-MX') + ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
            }
        } catch(e) {}

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${fechaCelda}</td>
            <td><strong>${mon.Nombre_Estudiante}</strong></td>
            <td><span style="background: rgba(255,159,67,0.15); color: #ff9f43; padding: 2px 6px; border-radius: 4px; font-weight: bold;">${mon.PH}</span></td>
            <td>${mon.Salinidad}</td>
            <td>${mon.Humedad}%</td>
            <td>${mon.Temperatura}°C</td>
            <td style="max-width: 300px; word-break: break-word; white-space: normal; text-align: left;">${mon.Observaciones}</td>
        `;
        tbody.appendChild(tr);
    });
}

function formatearFecha(fechaStr) {
    if (!fechaStr) return 'N/A';
    const date = new Date(fechaStr);
    return date.toLocaleDateString('es-MX');
}

// --- Lógica específica para la página de Inventario de Insumos (Materia Prima) ---

if (window.location.pathname.includes('productor_inventario.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        cargarInventarioInsumos();
        configurarFormularioInsumos();
    });
}

async function cargarInventarioInsumos() {
    const idProductor = localStorage.getItem('productor_id');
    try {
        const response = await fetch(`${API_BASE_URL}/api/productor/inventario?id_productor=${idProductor}&tipo=insumo`);
        if (response.ok) {
            const data = await response.json();
            
            // Inyectar KPIs de inventario
            document.getElementById('inv-kpi-critico').innerText = data.stats.critico;
            document.getElementById('inv-kpi-critico-desc').innerText = `Cantidad restante: ${data.stats.critico_cant}`;
            document.getElementById('inv-kpi-atencion').innerText = data.stats.atencion;
            document.getElementById('inv-kpi-estado').innerText = data.stats.estado;

            renderizarTablaInsumos(data.items);
        }
    } catch (error) {
        console.error('Error al cargar insumos:', error);
    }
}

function renderizarTablaInsumos(insumos) {
    const tbody = document.querySelector('.table-container table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    if (insumos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No hay insumos en tu inventario.</td></tr>';
        return;
    }

    insumos.forEach(ins => {
        const tr = document.createElement('tr');
        // Determinamos un color si el stock es bajo (ej. menos de 10)
        const isLow = ins.Cantidad < 10;
        tr.style.background = isLow ? 'rgba(239, 68, 68, 0.1)' : '';

        tr.innerHTML = `
            <td>${ins.Lote}</td>
            <td>${ins.Observaciones || 'General'}</td>
            <td><span style="${isLow ? 'color: #ef4444; font-weight: bold;' : ''}">${ins.Cantidad}</span></td>
            <td style="color: var(--accent-green);">Registrado</td>
            <td><button class="icon-btn" onclick="eliminarInsumo(${ins.Id_Inventario})" title="Eliminar registro"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg></button></td>
        `;
        tbody.appendChild(tr);
    });
}

function configurarFormularioInsumos() {
    const form = document.querySelector('.details-form');
    if (!form) return;

    form.onsubmit = null;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const idProductor = localStorage.getItem('productor_id');
        const parcelaSelect = document.getElementById('tierra-parcela');
        const parcela = parcelaSelect.options[parcelaSelect.selectedIndex].text;
        const ph = document.getElementById('tierra-ph').value;
        const p = document.getElementById('tierra-p').value;
        const k = document.getElementById('tierra-k').value;
        const ce = document.getElementById('tierra-ce').value;
        const humedad = document.getElementById('tierra-humedad').value;

        const data = {
            id_productor: idProductor,
            lote: `Registro Tierra: ${parcela}`,
            cantidad: 1, // Se registra como 1 entrada de bitácora
            precio: 0,
            observaciones: `pH: ${ph} | CE: ${ce} dS/m | P: ${p} | K: ${k} | Hum: ${humedad}%`
        };

        try {
            // Calcular IES
            let ies = 0;
            try {
                const iesRes = await fetch(`${API_BASE_URL}/api/calculos/estres`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ce_obs: parseFloat(ce), ce_umbral: 1.7, factor: 0.12 })
                });
                if (iesRes.ok) {
                    const iesData = await iesRes.json();
                    ies = iesData.resultado;
                }
            } catch (error) {
                console.warn('No se pudo calcular el IES', error);
            }

            const response = await fetch(`${API_BASE_URL}/api/productor/inventario`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                if (typeof mostrarAlerta === 'function') {
                    mostrarAlerta('success', 'Insumo Guardado', 'El insumo se ha registrado correctamente.');
                    if (ies > 50) {
                        setTimeout(() => {
                            mostrarAlerta('warning', '¡Peligro Crítico de Estrés Salino!', `El IES alcanzó ${ies.toFixed(1)}%. Se requiere un lavado de suelo urgente. Riesgo grave para la producción.`, 10000);
                        }, 1000);
                    }
                }
                form.reset();
                cargarInventarioInsumos();
            } else {
                alert('Error al registrar insumo.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

window.eliminarInsumo = async function(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este registro?')) return;
    
    const idProductor = localStorage.getItem('productor_id');
    try {
        const response = await fetch(`${API_BASE_URL}/api/productor/inventario/${id}?id_productor=${idProductor}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            if (typeof mostrarAlerta === 'function') {
                mostrarAlerta('success', 'Eliminado', 'El registro se ha eliminado correctamente.');
            } else {
                alert('Registro eliminado.');
            }
            cargarInventarioInsumos();
        } else {
            alert('No se pudo eliminar el registro.');
        }
    } catch (error) {
        console.error('Error al eliminar:', error);
    }
};
