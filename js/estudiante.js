// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:'
    ? 'http://127.0.0.1:5000'
    : '';

document.addEventListener('DOMContentLoaded', () => {
    // Fallback para recuperar sesión de los parámetros URL en modo file:// (cuando el localStorage está particionado por directorio)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('estudiante_id')) {
        localStorage.setItem('estudiante_id', urlParams.get('estudiante_id'));
    }
    if (urlParams.has('estudiante_nombre')) {
        localStorage.setItem('estudiante_nombre', urlParams.get('estudiante_nombre'));
    }

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
                    <td style="max-width: 300px; word-break: break-word; white-space: normal; text-align: left;">${mon.Observaciones}</td>
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

// Función para exportar la bitácora del estudiante a un archivo CSV (descarga directa)
async function exportarBitacoraCSV() {
    const estudianteId = localStorage.getItem('estudiante_id');
    if (!estudianteId) {
        alert('No se pudo identificar la sesión del estudiante.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/estudiante/monitoreos?id_estudiante=${estudianteId}`);
        const monitoreos = await response.json();

        if (!response.ok || !monitoreos || monitoreos.length === 0) {
            alert('No tienes registros de monitoreo para exportar aún.');
            return;
        }

        // Encabezado del CSV con BOM (para compatibilidad de acentos en Microsoft Excel)
        let csvContent = "\uFEFF";
        csvContent += "Fecha,Productor,pH,Salinidad (dS/m),Humedad (%),Temperatura (C),Observaciones\n";

        monitoreos.forEach(mon => {
            // Limpieza de caracteres de escape en observaciones
            const obsClean = (mon.Observaciones || "").replace(/"/g, '""').replace(/\r?\n|\r/g, " ");
            const row = `"${mon.Fecha}","${mon.Nombre_Productor}",${mon.PH},${mon.Salinidad},${mon.Humedad},${mon.Temperatura},"${obsClean}"`;
            csvContent += row + "\n";
        });

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", `Bitacora_Monitoreo_Estudiante_${estudianteId}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error al exportar bitácora a CSV:', error);
        alert('Ocurrió un error al generar la descarga del archivo CSV.');
    }
}

// Analizar la aptitud del suelo comparando los datos contra el catálogo general de semillas
async function analizarAptitudSuelo() {
    const inputPh = parseFloat(document.getElementById('calc-ph').value);
    const inputSal = parseFloat(document.getElementById('calc-salinidad').value);
    
    if (isNaN(inputPh) || isNaN(inputSal)) {
        alert('Por favor, ingresa valores numéricos de pH y salinidad válidos.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/semillas`);
        const semillas = await response.json();
        
        if (!response.ok) {
            alert('No se pudo acceder al catálogo de semillas del servidor.');
            return;
        }
        
        const recomendados = [];
        const advertencias = [];
        
        semillas.forEach(sem => {
            const phOpt = parseFloat(sem.pH_Optimo || 6.5);
            const diffPh = Math.abs(inputPh - phOpt);
            
            // Fórmulas de aptitud coincidentes con los modelos agronómicos del backend
            let factorPh = 1.0;
            if (diffPh <= 0.5) {
                factorPh = 1.0;
            } else if (diffPh <= 1.2) {
                factorPh = 1.0 - (diffPh - 0.5) * 0.35;
            } else {
                factorPh = Math.max(0.15, 0.75 - (diffPh - 1.2) * 0.30);
            }
            
            let factorSal = 1.0;
            if (inputSal <= 1.5) {
                factorSal = 1.0;
            } else if (inputSal <= 3.0) {
                factorSal = 1.0 - (inputSal - 1.5) * 0.20;
            } else {
                factorSal = Math.max(0.20, 0.70 - (inputSal - 3.0) * 0.15);
            }
            
            const aptitud = factorPh * factorSal * 100;
            
            if (aptitud >= 75) {
                recomendados.push({ nombre: sem.Nombre_Semilla, aptitud: Math.round(aptitud) });
            } else {
                advertencias.push({ nombre: sem.Nombre_Semilla, aptitud: Math.round(aptitud), phOpt: phOpt });
            }
        });
        
        // Ordenar por nivel de idoneidad
        recomendados.sort((a, b) => b.aptitud - a.aptitud);
        advertencias.sort((a, b) => a.aptitud - b.aptitud);
        
        // Renderizar los resultados en las dos columnas
        const container = document.getElementById('aptitud-resultados-container');
        const grid = document.getElementById('aptitud-listas-grid');
        
        container.style.display = 'block';
        
        let htmlRecomendados = `
            <div>
                <h4 style="color: var(--accent-green, #2ec4b6); margin-bottom: 12px; font-weight: 700; font-size: 0.95rem;">Cultivos Recomendados (Alto Éxito):</h4>
                <div style="max-height: 250px; overflow-y: auto; border: 2px solid #000; border-radius: 6px; padding: 10px; background: #f0fdf4; box-shadow: 2px 2px 0px #000;">
                    <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.8;">
        `;
        if (recomendados.length === 0) {
            htmlRecomendados += '<li style="color:#718096; font-size:0.9rem;">No hay cultivos óptimos recomendados para estas condiciones de suelo.</li>';
        } else {
            recomendados.forEach(item => {
                htmlRecomendados += `<li style="margin-bottom: 5px; display:flex; justify-content:space-between; font-size:0.9rem; border-bottom: 1px dashed rgba(0,0,0,0.1); padding-bottom:3px;">
                    <span><strong>${item.nombre}</strong></span>
                    <span style="color: #2ec4b6; font-weight: 700;">${item.aptitud}% apto</span>
                </li>`;
            });
        }
        htmlRecomendados += `</ul></div></div>`;
        
        let htmlAdvertencias = `
            <div>
                <h4 style="color: #ef4444; margin-bottom: 12px; font-weight: 700; font-size: 0.95rem;">No Recomendados / Con Alerta:</h4>
                <div style="max-height: 250px; overflow-y: auto; border: 2px solid #000; border-radius: 6px; padding: 10px; background: #fef2f2; box-shadow: 2px 2px 0px #000;">
                    <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.8;">
        `;
        if (advertencias.length === 0) {
            htmlAdvertencias += '<li style="color:#718096; font-size:0.9rem;">No hay cultivos de riesgo para estas condiciones de suelo.</li>';
        } else {
            advertencias.forEach(item => {
                htmlAdvertencias += `<li style="margin-bottom: 5px; display:flex; justify-content:space-between; font-size:0.9rem; border-bottom: 1px dashed rgba(0,0,0,0.1); padding-bottom:3px;">
                    <span><strong>${item.nombre}</strong> <span style="font-size:0.75rem; color:#718096;">(Opt: ${item.phOpt})</span></span>
                    <span style="color: #ef4444; font-weight: 700;">${item.aptitud}% apto</span>
                </li>`;
            });
        }
        htmlAdvertencias += `</ul></div></div>`;
        
        grid.innerHTML = htmlRecomendados + htmlAdvertencias;
        
    } catch (error) {
        console.error('Error al analizar aptitud del suelo:', error);
        alert('No se pudo conectar al catálogo de semillas del servidor.');
    }
}
