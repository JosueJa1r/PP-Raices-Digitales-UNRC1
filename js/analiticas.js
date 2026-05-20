// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    cargarAnaliticas();
});

async function cargarAnaliticas() {
    console.log('Intentando cargar analíticas desde:', `${API_BASE_URL}/api/analiticas/global`);
    try {
        const response = await fetch(`${API_BASE_URL}/api/analiticas/global`);
        
        if (!response.ok) {
            throw new Error(`Error en el servidor: ${response.status}`);
        }

        const data = await response.json();
        console.log('Datos recibidos:', data);
        
        // Inyectar KPIs (con seguridad)
        if (data.kpis) {
            document.getElementById('kpi-riesgo').innerText = data.kpis.riesgo || 'N/A';
            document.getElementById('kpi-oportunidad').innerText = data.kpis.oportunidad || 'N/A';
            document.getElementById('kpi-total').innerText = data.kpis.total_agricultores || 0;
        }
        
        renderizarGraficas(data);
        poblarTabla(data);
        
    } catch (error) {
        console.error('Error detallado al cargar analíticas:', error);
        mostrarAlerta('error', 'Error de Carga', 'No se pudo conectar con el servidor de analíticas. Asegúrate de que el backend esté corriendo.');
    }
}

function renderizarGraficas(data) {
    const textColor = '#fff'; // White text to match the beautiful dark/green glassmorphism background
    const gridColor = 'rgba(255,255,255,0.08)';

    // 1. Gráfica de Volumen (Semillas Más Plantadas)
    const ctxVolumen = document.getElementById('chartTemporada').getContext('2d');
    const labelsVol = data.volumen.length > 0 ? data.volumen.map(v => v.Nombre_Semilla) : ['Sin datos'];
    const valuesVol = data.volumen.length > 0 ? data.volumen.map(v => v.Total_Hectareas) : [0];
    
    const backgroundColors = valuesVol.map((v, i) => i === 0 && v > 0 ? 'rgba(22, 163, 74, 0.85)' : 'rgba(74, 222, 128, 0.65)');
    const borderColors = valuesVol.map((v, i) => i === 0 && v > 0 ? '#16a34a' : '#4ade80');

    new Chart(ctxVolumen, {
        type: 'bar',
        data: {
            labels: labelsVol,
            datasets: [{
                label: 'Cantidad Sembrada/Cosechada',
                data: valuesVol,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { 
                    beginAtZero: true, 
                    grid: { color: gridColor }, 
                    ticks: { color: textColor },
                    title: { display: true, text: 'Hectáreas (ha)', color: textColor }
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: textColor } 
                }
            },
            plugins: { 
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` Cantidad: ${context.raw} ha`;
                        }
                    }
                }
            }
        }
    });

    // 2. Gráfica de Valor Ganado por Cultivo
    const ctxInversion = document.getElementById('chartValor').getContext('2d');
    new Chart(ctxInversion, {
        type: 'doughnut',
        data: {
            labels: data.inversion.length > 0 ? data.inversion.map(i => i.Nombre_Semilla) : ['Sin datos'],
            datasets: [{
                data: data.inversion.length > 0 ? data.inversion.map(i => i.Total_Valor) : [0],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6', '#ec4899'],
                borderWidth: 2,
                borderColor: '#1e293b'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { position: 'bottom', labels: { color: textColor, padding: 15 } },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` Valor Ganado: $${context.raw.toLocaleString('es-MX')} MXN`;
                        }
                    }
                }
            }
        }
    });

    // 3. Gráfica de Top Productores: Extensión (m²) y Ganancia ($)
    const ctxTop = document.getElementById('chartAgricultores').getContext('2d');
    new Chart(ctxTop, {
        type: 'bar',
        data: {
            labels: data.top_productores.length > 0 ? data.top_productores.map(p => p.Nombre) : ['Nadie aún'],
            datasets: [
                {
                    label: 'Área (m²)',
                    data: data.top_productores.length > 0 ? data.top_productores.map(p => p.Metros_Cuadrados) : [0],
                    xAxisID: 'x',
                    backgroundColor: 'rgba(74, 222, 128, 0.8)',
                    borderColor: '#4ade80',
                    borderWidth: 1.5,
                    borderRadius: 4
                },
                {
                    label: 'Ganancia por Cosecha ($)',
                    data: data.top_productores.length > 0 ? data.top_productores.map(p => p.Ganancia) : [0],
                    xAxisID: 'x2',
                    backgroundColor: 'rgba(245, 158, 11, 0.8)',
                    borderColor: '#d97706',
                    borderWidth: 1.5,
                    borderRadius: 4
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { 
                    position: 'bottom',
                    beginAtZero: true, 
                    grid: { color: gridColor }, 
                    ticks: { color: textColor },
                    title: { display: true, text: 'Área (m²)', color: textColor }
                },
                x2: { 
                    position: 'top',
                    beginAtZero: true, 
                    grid: { drawOnChartArea: false }, 
                    ticks: { color: textColor },
                    title: { display: true, text: 'Ganancia ($ MXN)', color: textColor }
                },
                y: { 
                    grid: { display: false }, 
                    ticks: { color: textColor } 
                }
            },
            plugins: { 
                legend: { 
                    display: true,
                    labels: { color: textColor, padding: 10 }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.dataset.label.includes('Área')) {
                                return ` Área: ${context.raw.toLocaleString('es-MX')} m²`;
                            } else {
                                return ` Ganancia: $${context.raw.toLocaleString('es-MX')} MXN`;
                            }
                        }
                    }
                }
            }
        }
    });
}

function poblarTabla(data) {
    const tbody = document.querySelector('table tbody');
    if (!tbody) return;

    if (data.volumen.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 2rem;">No hay cultivos registrados en el sistema actualmente.</td></tr>';
        return;
    }

    tbody.innerHTML = '';
    data.volumen.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.Nombre_Semilla}</td>
            <td>${item.Nombre_Categoria || 'General'}</td>
            <td>${item.Total_Hectareas}</td>
            <td>$${item.Valor_Semilla ? item.Valor_Semilla.toLocaleString('es-MX') : '--'} MXN</td>
        `;
        tbody.appendChild(tr);
    });
}
