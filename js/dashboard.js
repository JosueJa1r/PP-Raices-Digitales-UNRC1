// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    cargarDatosDashboard();
});

async function cargarDatosDashboard() {
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

        // 2. Cargar Cosechas
        const responseCosechas = await fetch(`${API_BASE_URL}/api/productor/cosechas?id_productor=${idProductor}`);
        if (responseCosechas.ok) {
            const cosechas = await responseCosechas.json();
            renderizarCosechas(cosechas);
        }

        // 3. Cargar Semillas (Inventario Personal del Agricultor)
        const responseSemillas = await fetch(`${API_BASE_URL}/api/semillas?id_productor=${idProductor}`);
        if (responseSemillas.ok) {
            const semillas = await responseSemillas.json();
            renderizarSemillas(semillas);
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

function renderizarCosechas(cosechas) {
    const tbody = document.querySelector('.table-container table tbody');
    if (!tbody) return;

    // Limpiar tabla
    tbody.innerHTML = '';

    if (cosechas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No hay cosechas registradas.</td></tr>';
        return;
    }

    cosechas.forEach(cos => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${cos.Id_Cosecha || 'N/A'}</td>
            <td>${cos.Temporada || 'General'}</td>
            <td><span class="status-badge status-${cos.Estado === 'Activa' ? 'active' : 'finished'}">${cos.Estado || 'Desconocido'}</span></td>
            <td>${formatearFecha(cos.Fecha_Inicio)}</td>
            <td>${formatearFecha(cos.Fecha_Fin)}</td>
            <td style="color: var(--accent-green); font-weight: bold;">+${cos.roi_calculado}%</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderizarSemillas(semillas) {
    const tables = document.querySelectorAll('.table-container table');
    if (tables.length < 2) return;
    
    const tbody = tables[1].querySelector('tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (semillas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No tienes semillas en tu inventario.</td></tr>';
        return;
    }

    semillas.forEach((sem, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>SEM-${(index + 1).toString().padStart(3, '0')}</td>
            <td>${sem.Nombre_Semilla}</td>
            <td>${sem.Nombre_Categoria || 'Semillas'}</td>
            <td>N/A</td>
            <td>${sem.Cantidad || 0} Unidades</td>
        `;
        tbody.appendChild(tr);
    });
}

function formatearFecha(fechaStr) {
    if (!fechaStr) return 'N/A';
    const date = new Date(fechaStr);
    return date.toLocaleDateString('es-MX');
}

// --- Lógica específica para la página de Cosechas (Inventario de Venta) ---

if (window.location.pathname.includes('productor_cosechas.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        cargarInventarioVenta();
        configurarFormularioInventario();
    });
}

async function cargarInventarioVenta() {
    const idProductor = localStorage.getItem('productor_id');
    try {
        const response = await fetch(`${API_BASE_URL}/api/productor/inventario?id_productor=${idProductor}`);
        if (response.ok) {
            const productos = await response.json();
            renderizarInventarioVenta(productos);
        }
    } catch (error) {
        console.error('Error al cargar inventario:', error);
    }
}

function renderizarInventarioVenta(productos) {
    const tbody = document.querySelector('.table-container table tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    productos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.Lote}</td>
            <td>General</td>
            <td>${p.Cantidad} Unidades</td>
            <td>$${p.Precio_Actual} MXN</td>
            <td><span style="color: var(--accent-green);">Publicado</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function configurarFormularioInventario() {
    const form = document.querySelector('.details-form');
    if (!form) return;

    form.onsubmit = null; // Quitar el preventDefault de ejemplo del HTML
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const idProductor = localStorage.getItem('productor_id');
        const lote = form.querySelector('input[type="text"]').value;
        const cantidad = form.querySelector('input[placeholder="Ej. 100"]').value;
        const precio = form.querySelector('input[step="0.50"]').value;

        const data = {
            id_productor: idProductor,
            lote: lote,
            cantidad: cantidad,
            precio: precio,
            observaciones: 'Registro desde panel'
        };

        try {
            const response = await fetch(`${API_BASE_URL}/api/productor/inventario`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                if (typeof mostrarAlerta === 'function') {
                    mostrarAlerta('success', 'Éxito', 'Producto registrado correctamente.');
                } else {
                    alert('Producto registrado correctamente.');
                }
                form.reset();
                cargarInventarioVenta();
            } else {
                alert('Error al registrar producto.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
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
        const response = await fetch(`${API_BASE_URL}/api/productor/inventario?id_productor=${idProductor}`);
        if (response.ok) {
            const data = await response.json();
            
            // Inyectar KPIs de inventario
            document.getElementById('inv-kpi-critico').innerText = data.stats.critico;
            document.getElementById('inv-kpi-critico-desc').innerText = `Quedan solo ${data.stats.critico_cant} unidades`;
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
            <td>General</td>
            <td><span style="${isLow ? 'color: #ef4444; font-weight: bold;' : ''}">${ins.Cantidad} Unidades</span></td>
            <td style="color: #f59e0b;">$${ins.merma_proyectada.toFixed(2)}</td>
            <td><button class="icon-btn"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg></button></td>
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
        const nombre = form.querySelector('input[type="text"]').value;
        const cantidad = form.querySelector('input[placeholder="Ej. 10"]').value;
        const ph = form.querySelector('input[placeholder="Ej. 6.5"]').value;

        const data = {
            id_productor: idProductor,
            lote: nombre,
            cantidad: cantidad,
            precio: 0, // Los insumos no suelen tener precio de venta aquí
            observaciones: `pH Óptimo: ${ph}`
        };

        try {
            const response = await fetch(`${API_BASE_URL}/api/productor/inventario`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                if (typeof mostrarAlerta === 'function') {
                    mostrarAlerta('success', 'Insumo Guardado', 'El insumo se ha registrado correctamente.');
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
