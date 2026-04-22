// Configuración de colores globales para Chart.js
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Inter', sans-serif";
        const greenAccent = '#10b981';
        const cyanAccent = '#06b6d4';
        const blueAccent = '#3b82f6';
        const redAccent = '#ef4444';
        const gridColor = 'rgba(255, 255, 255, 0.05)';

        // 1. Gráfica de Barras: Temporada vs Producto
        const ctxTemporada = document.getElementById('chartTemporada').getContext('2d');
        new Chart(ctxTemporada, {
            type: 'bar',
            data: {
                labels: ['Maíz Blanco', 'Tomate Saladette', 'Aguacate Hass', 'Frijol Pinto', 'Chile Jalapeño'],
                datasets: [
                    {
                        label: 'Primavera',
                        data: [600, 150, 400, 50, 100],
                        backgroundColor: cyanAccent,
                    },
                    {
                        label: 'Verano',
                        data: [500, 250, 400, 100, 150],
                        backgroundColor: greenAccent,
                    },
                    {
                        label: 'Otoño/Invierno',
                        data: [150, 50, 0, 150, 50],
                        backgroundColor: blueAccent,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: gridColor }
                    },
                    x: {
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });

        // 2. Gráfica de Pastel: Valor de Semilla
        const ctxValor = document.getElementById('chartValor').getContext('2d');
        new Chart(ctxValor, {
            type: 'doughnut',
            data: {
                labels: ['Semilla Premium (Alta Inversión)', 'Semilla Estándar', 'Semilla Criolla/Baja Inversión'],
                datasets: [{
                    data: [35, 50, 15],
                    backgroundColor: [cyanAccent, greenAccent, blueAccent],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        // 3. Gráfica Barras Horizontales: Usuarios Agricultores
        const ctxAgricultores = document.getElementById('chartAgricultores').getContext('2d');
        new Chart(ctxAgricultores, {
            type: 'bar',
            data: {
                labels: ['Productor A (Norte)', 'Finca Las Marías', 'Productor C', 'AgroTech', 'Rancho El Sol'],
                datasets: [{
                    label: 'Hectáreas Plantadas',
                    data: [450, 320, 210, 180, 45.5],
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: blueAccent,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: gridColor }
                    },
                    y: {
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });