/**
 * Sistema Global de Alertas (Toasts) para Raíces Digitales
 */

// Inyectar el contenedor de toasts al cargar el script si no existe
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
});

/**
 * Muestra una notificación flotante.
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 * @param {string} titulo - Título de la alerta
 * @param {string} mensaje - Mensaje descriptivo
 * @param {number} duracion - Tiempo en ms antes de desaparecer (default 4000)
 */
function mostrarAlerta(tipo, titulo, mensaje, duracion = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    // Configurar iconos según el tipo
    const iconos = {
        'success': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
        'error': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
        'warning': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
        'info': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
    };

    const iconoHTML = iconos[tipo] || iconos['info'];
    const claseTipo = `toast-${tipo}`;

    // Crear el elemento HTML
    const toast = document.createElement('div');
    toast.className = `toast ${claseTipo}`;
    toast.innerHTML = `
        <div class="toast-icon">${iconoHTML}</div>
        <div class="toast-content">
            <span class="toast-title">${titulo}</span>
            <span class="toast-message">${mensaje}</span>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    // Añadir al contenedor
    container.appendChild(toast);

    // Animación de entrada
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // Auto-eliminar después de X tiempo
    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        
        // Esperar a que termine la animación css para quitar del DOM
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 400); // 400ms es el tiempo de la transición CSS
    }, duracion);
}
