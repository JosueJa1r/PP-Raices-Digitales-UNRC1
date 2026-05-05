// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    cargarAnaliticas();
});

async function cargarAnaliticas() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/analiticas/global`);
        if (response.ok) {
            const data = await response.json();
            
            // Inyectar KPIs
            document.getElementById('kpi-riesgo').innerText = data.kpis.riesgo;
            document.getElementById('kpi-oportunidad').innerText = data.kpis.oportunidad;
            document.getElementById('kpi-total').innerText = data.kpis.total_agricultores;
            
            renderizarGraficas(data);
        }
    } catch (error) {
        console.error('Error al cargar analíticas:', error);
    }
}

function renderizarGraficas(data) {
    // 1. Gráfica de Volumen (Barras)
    const ctxVolumen = document.getElementById('chartTemporada').getContext('2d');
    new Chart(ctxVolumen, {
        type: 'bar',
        data: {
            labels: data.volumen.map(v => v.Nombre_Semilla),
            datasets: [{
                label: 'Hectáreas Totales',
                data: data.volumen.map(v => v.Total_Hectareas),
                backgroundColor: 'rgba(74, 222, 128, 0.5)',
                borderColor: '#4ade80',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#fff' } },
                x: { ticks: { color: '#fff' } }
            },
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });

    // 2. Gráfica de Inversión (Doughnut)
    const ctxInversion = document.getElementById('chartValor').getContext('2d');
    new Chart(ctxInversion, {
        type: 'doughnut',
        data: {
            labels: data.inversion.map(i => i.Nombre_Semilla),
            datasets: [{
                data: data.inversion.map(i => i.Total_Valor),
                backgroundColor: [
                    '#4ade80', '#22c55e', '#16a34a', '#15803d', '#14532d'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'right', labels: { color: '#fff' } } }
        }
    });

    // 3. Gráfica de Top Productores (Horizontal Bar)
    const ctxTop = document.getElementById('chartAgricultores').getContext('2d');
    new Chart(ctxTop, {
        type: 'bar',
        data: {
            labels: data.top_productores.map(p => p.Nombre),
            datasets: [{
                label: 'Hectáreas',
                data: data.top_productores.map(p => p.Extension),
                backgroundColor: 'rgba(245, 158, 11, 0.5)',
                borderColor: '#f59e0b',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#fff' } },
                y: { ticks: { color: '#fff' } }
            },
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });
}