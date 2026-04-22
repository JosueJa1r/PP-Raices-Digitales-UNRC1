const initClima = () => {
    const climaWidget = document.getElementById('widget-clima');
    if (!climaWidget) return;

    // Coordenadas aproximadas de Xochimilco, CDMX
    const lat = 19.2642;
    const lon = -99.1026;
    
    // API Open-Meteo (Gratuita, no requiere KEY)
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,is_day,precipitation,weather_code&timezone=America%2FMexico_City`;

    // Códigos WMO de clima simplificados para íconos/descripciones
    const interpretarClima = (codigo, deDia) => {
        if (codigo === 0) return { texto: 'Despejado', icono: deDia ? '☀️' : '🌙' };
        if (codigo >= 1 && codigo <= 3) return { texto: 'Nublado', icono: '☁️' };
        if (codigo >= 51 && codigo <= 67) return { texto: 'Lluvia Ligera', icono: '🌦️' };
        if (codigo >= 80 && codigo <= 82) return { texto: 'Tormenta/Lluvia Fuerte', icono: '⛈️' };
        return { texto: 'Variable', icono: '⛅' };
    };

    const darConsejo = (temp, lluvia, climaStr) => {
        if (lluvia > 0 || climaStr.includes('Lluvia')) return "No es necesario regar las chinampas hoy.";
        if (temp > 28) return "Temperatura alta. Riego sugerido al atardecer.";
        if (temp < 10) return "Temperatura baja. Protege brotes jóvenes de posibles heladas.";
        return "Condiciones óptimas para trabajo de campo.";
    };

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const current = data.current;
            const climaInfo = interpretarClima(current.weather_code, current.is_day);
            const consejo = darConsejo(current.temperature_2m, current.precipitation, climaInfo.texto);

            climaWidget.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 2.5rem; line-height: 1;">${climaInfo.icono}</span>
                        <div>
                            <h3 style="margin: 0; font-size: 1.8rem; color: #fff;">${current.temperature_2m}°C</h3>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--text-muted);">Xochimilco, CDMX</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: var(--accent-green); font-weight: 600;">${climaInfo.texto}</p>
                        <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Humedad: ${current.relative_humidity_2m}%</p>
                    </div>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 6px; border-left: 3px solid var(--accent-green);">
                    <p style="margin: 0; font-size: 0.85rem; color: #fff;"><strong>Consejo Agrícola:</strong> ${consejo}</p>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error cargando el clima:', error);
            climaWidget.innerHTML = `<p style="color: #ef4444;">Error al cargar datos meteorológicos.</p>`;
        });
};

initClima();
