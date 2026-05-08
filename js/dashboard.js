// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('productor_dashboard.html')) {
        cargarDatosDashboard();
    }
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
        const response = await fetch(`${API_BASE_URL}/api/productor/inventario?id_productor=${idProductor}&tipo=cosecha`);
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
        
        let loteDisplay = p.Lote;
        let unidadDisplay = 'Unidades';
        const match = p.Lote.match(/\(([^)]+)\)$/);
        if (match) {
            unidadDisplay = match[1];
            loteDisplay = p.Lote.replace(/\s*\([^)]+\)$/, '');
        }

        tr.innerHTML = `
            <td>${loteDisplay}</td>
            <td>General</td>
            <td>${p.Cantidad} ${unidadDisplay}</td>
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
        const humedad = document.getElementById('tierra-humedad').value;

        const data = {
            id_productor: idProductor,
            lote: `Registro Tierra: ${parcela}`,
            cantidad: 1, // Se registra como 1 entrada de bitácora
            precio: 0,
            observaciones: `pH: ${ph} | P: ${p} | K: ${k} | Humedad: ${humedad}%`
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
