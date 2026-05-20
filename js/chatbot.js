const initChatbot = () => {
    const isClient = window.location.pathname.includes('cliente');
    const greetingMessage = isClient 
        ? '¡Hola! Soy tu asistente inteligente. ¿En qué te puedo ayudar hoy? Prueba preguntarme sobre "productos", "envíos" o "recomendaciones".'
        : '¡Hola, productor! Soy tu asistente inteligente. ¿En qué te puedo ayudar hoy? Prueba preguntarme sobre "clima", "ventas" o "consejo".';

    // Inyectar el HTML del Chatbot en el body
    const botHTML = `
        <div id="chatbot-container" class="chatbot-container chatbot-hidden">
            <div class="chatbot-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="bot-avatar">🤖</div>
                    <div>
                        <h4 style="margin: 0; color: #fff;">RaícesBot IA</h4>
                        <span style="font-size: 0.75rem; color: var(--accent-green);">En línea</span>
                    </div>
                </div>
                <button id="chatbot-close-btn" aria-label="Cerrar chat">&times;</button>
            </div>
            <div id="chatbot-messages" class="chatbot-messages">
                <div class="bot-message">${greetingMessage}</div>
            </div>
            <div class="chatbot-input-area">
                <input type="text" id="chatbot-input" placeholder="Escribe tu consulta...">
                <button id="chatbot-send-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
            </div>
        </div>
        <button id="chatbot-fab" class="chatbot-fab" aria-label="Abrir asistente">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
        </button>
    `;

    document.body.insertAdjacentHTML('beforeend', botHTML);

    const container = document.getElementById('chatbot-container');
    const fab = document.getElementById('chatbot-fab');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const sendBtn = document.getElementById('chatbot-send-btn');
    const inputField = document.getElementById('chatbot-input');
    const messagesDiv = document.getElementById('chatbot-messages');

    // Toggle Chatbot
    fab.addEventListener('click', () => {
        container.classList.remove('chatbot-hidden');
        fab.style.transform = 'scale(0)';
    });

    closeBtn.addEventListener('click', () => {
        container.classList.add('chatbot-hidden');
        fab.style.transform = 'scale(1)';
    });

    const addMessage = (text, isUser) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = isUser ? 'user-message' : 'bot-message';
        msgDiv.textContent = text;
        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000'
        : '';

    const handleSend = async () => {
        const text = inputField.value.trim();
        if (!text) return;
        
        addMessage(text, true);
        inputField.value = '';

        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing';
        typingDiv.textContent = 'Escribiendo...';
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        try {
            // Recopilar contexto si es productor
            const payload = { message: text };
            if (!isClient) {
                const idProductor = localStorage.getItem('productor_id');
                if (idProductor) {
                    payload.id_productor = parseInt(idProductor);
                }
            }

            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            messagesDiv.removeChild(typingDiv);
            
            if (response.ok) {
                // Formatear la respuesta (reemplazar saltos de línea y formatear Markdown básico si es necesario)
                let replyText = data.reply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
                const msgDiv = document.createElement('div');
                msgDiv.className = 'bot-message';
                msgDiv.innerHTML = replyText;
                messagesDiv.appendChild(msgDiv);
            } else {
                addMessage(data.error || 'Hubo un error al procesar tu solicitud.', false);
            }
        } catch (error) {
            console.error('Error al contactar al backend:', error);
            messagesDiv.removeChild(typingDiv);
            addMessage('Error de conexión. Asegúrate de que el servidor local (app.py) esté corriendo en el puerto 5000.', false);
        }
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    sendBtn.addEventListener('click', handleSend);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
};

// Ejecutar inmediatamente ya que el script está al final del body
initChatbot();
