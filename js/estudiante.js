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

// ─── Modelos Científicos: Integración y Probabilidad Bayesiana ─────

async function autocompletarClimaFormulario() {
    // Coordenadas aproximadas de las Chinampas de Xochimilco
    const lat = 19.2638;
    const lon = -99.102;
    // Pedimos temperatura actual, humedad relativa y humedad del suelo
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m&hourly=soil_moisture_0_to_1cm&timezone=America/Mexico_City`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok && data.current) {
            const temp = data.current.temperature_2m;
            const humAire = data.current.relative_humidity_2m;
            
            // Intentar obtener humedad del suelo de la hora actual
            let humSuelo = humAire;
            if (data.hourly && data.hourly.soil_moisture_0_to_1cm) {
                const now = new Date();
                const currentHour = now.getHours();
                const soilVal = data.hourly.soil_moisture_0_to_1cm[currentHour];
                if (soilVal !== undefined) {
                    // Convertir de m³/m³ a porcentaje
                    humSuelo = Math.round(soilVal * 1000) / 10;
                }
            }
            
            document.getElementById('form-temperatura').value = temp;
            document.getElementById('form-humedad').value = humSuelo;
            
            // Añadir nota a las observaciones
            const obsEl = document.getElementById('form-observaciones');
            const notice = "[Clima autocompletado vía Open-Meteo]";
            if (!obsEl.value.includes(notice)) {
                obsEl.value = obsEl.value ? obsEl.value + " " + notice : notice;
            }
            
            alert(`¡Clima cargado con éxito para Xochimilco desde la API Open-Meteo!\n\n• Temperatura: ${temp}°C\n• Humedad del suelo estimada: ${humSuelo}%`);
        } else {
            alert('No se pudo obtener datos del clima desde Open-Meteo.');
        }
    } catch (error) {
        console.error('Error al autocompletar clima:', error);
        alert('Error al conectar con la API de Open-Meteo.');
    }
}

async function obtenerLluviaRealOpenMeteo() {
    const integralInput = document.getElementById('integral-tasas');
    
    // Coordenadas aproximadas de las Chinampas de Xochimilco: 19.2638, -99.102
    const lat = 19.2638;
    const lon = -99.102;
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=precipitation_sum&past_days=7&timezone=America/Mexico_City`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok && data.daily && data.daily.precipitation_sum) {
            // Tomamos los últimos 7 días de registros históricos de lluvia (excluyendo hoy que puede estar incompleto)
            const rainData = data.daily.precipitation_sum.slice(0, 7);
            integralInput.value = rainData.join(', ');
            alert('¡Datos de precipitación reales cargados con éxito desde Open-Meteo para Xochimilco!');
            calcularIntegralLluvia();
        } else {
            alert('No se pudo obtener datos válidos de Open-Meteo. Usando valores por defecto.');
        }
    } catch (error) {
        console.error('Error al consultar Open-Meteo:', error);
        alert('Error de conexión con la API de Open-Meteo.');
    }
}

async function calcularIntegralLluvia() {
    const input = document.getElementById('integral-tasas').value;
    const resEl = document.getElementById('integral-resultado');
    const container = document.getElementById('riemann-container');

    const rates = input.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));

    if (rates.length === 0) {
        alert('Ingresa una lista de números válidos separados por comas.');
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/api/calculos/integral`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tasas: rates })
        });
        const data = await res.json();
        
        if (res.ok) {
            resEl.innerText = `Resultado: ${data.resultado} ${data.unidad}`;
            
            // Dibujar las barras de Riemann de forma dinámica
            container.innerHTML = '';
            const maxRate = Math.max(...rates, 1);
            
            rates.forEach((rate, i) => {
                const bar = document.createElement('div');
                const heightPercent = (rate / maxRate) * 100;
                
                bar.style.height = `${Math.max(heightPercent, 5)}%`;
                bar.style.width = '30px';
                bar.style.background = 'rgba(255, 159, 67, 0.7)';
                bar.style.border = '2px solid #ff9f43';
                bar.style.borderRadius = '4px 4px 0 0';
                bar.style.position = 'relative';
                bar.style.cursor = 'pointer';
                bar.title = `Día ${i+1}: ${rate} mm/día`;
                
                // Efecto hover
                bar.addEventListener('mouseenter', () => {
                    bar.style.background = '#ff9f43';
                    bar.style.boxShadow = '0 0 8px rgba(255, 159, 67, 0.6)';
                });
                bar.addEventListener('mouseleave', () => {
                    bar.style.background = 'rgba(255, 159, 67, 0.7)';
                    bar.style.boxShadow = 'none';
                });

                container.appendChild(bar);
            });
        } else {
            resEl.innerText = `Error: ${data.error}`;
        }
    } catch (e) {
        console.error(e);
        resEl.innerText = 'Error al conectar con la API de Integral.';
    }
}

async function calcularProbabilidadBayesiana() {
    const pa = parseFloat(document.getElementById('bayes-pa').value);
    const pba = parseFloat(document.getElementById('bayes-pba').value);
    const pb = parseFloat(document.getElementById('bayes-pb').value);
    const resEl = document.getElementById('bayes-resultado');
    const barEl = document.getElementById('bayes-bar');

    if (isNaN(pa) || isNaN(pba) || isNaN(pb) || pb <= 0) {
        alert('Por favor ingresa valores de probabilidad válidos.');
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/api/calculos/bayes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ p_exito: pa, p_clima_exito: pba, p_clima: pb })
        });
        const data = await res.json();
        
        if (res.ok) {
            let resultado = data.resultado;
            if (resultado > 100) resultado = 100; // Límite matemático coherente
            
            resEl.innerText = `Resultado: ${resultado.toFixed(2)} ${data.unidad}`;
            barEl.style.width = `${resultado}%`;

            // Escala de colores según el nivel de éxito
            if (resultado >= 70) {
                barEl.style.background = '#2ec4b6'; // verde azulado ecológico
            } else if (resultado >= 40) {
                barEl.style.background = '#ff9f43'; // naranja estudiante
            } else {
                barEl.style.background = '#e71d36'; // rojo
            }
        } else {
            resEl.innerText = `Error: ${data.error}`;
        }
    } catch (e) {
        console.error(e);
        resEl.innerText = 'Error al conectar con la API de Bayes.';
    }
}

// Inicializar simulaciones al cargar la página
window.addEventListener('load', () => {
    setTimeout(() => {
        calcularIntegralLluvia();
        calcularProbabilidadBayesiana();
    }, 500);
});
