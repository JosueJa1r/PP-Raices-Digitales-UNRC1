const initChatbot = () => {
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
                <div class="bot-message">¡Hola, productor! Soy tu asistente inteligente. ¿En qué te puedo ayudar hoy? Prueba preguntarme sobre "clima", "ventas" o "consejo".</div>
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

    const getBotResponse = (text) => {
        const lowerText = text.toLowerCase();
        
        if (lowerText.includes('clima') || lowerText.includes('lluvia')) {
            return "Según los pronósticos de Open-Meteo para Xochimilco, estamos esperando clima variable. Te recomiendo revisar el widget superior en tu Dashboard. ¿Necesitas un consejo de riego?";
        }
        if (lowerText.includes('consejo') || lowerText.includes('riego')) {
            return "Mi análisis sugiere que para las chinampas, el riego matutino reduce el riesgo de hongos por la humedad de los canales. Aplícalo especialmente en tus macetas de Cempasúchil.";
        }
        if (lowerText.includes('ventas') || lowerText.includes('sobreproduccion') || lowerText.includes('competencia')) {
            return "Noté en el Explorador de Mercado que 4 productores de tu zona están cultivando Rábano. Podría haber sobreproducción el próximo mes. Te sugiero enfocar tus esfuerzos en plantas medicinales.";
        }
        if (lowerText.includes('gracias')) {
            return "¡De nada! Estoy aquí 24/7 para ayudarte a mejorar el rendimiento de tu rancho.";
        }
        
        return "Es una consulta interesante. Actualmente estoy analizando los datos históricos de tu chinampa. Por ahora, te sugiero mantener tu inventario de insumos actualizado para evitar desabastos.";
    };

    const addMessage = (text, isUser) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = isUser ? 'user-message' : 'bot-message';
        msgDiv.textContent = text;
        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    const handleSend = () => {
        const text = inputField.value.trim();
        if (!text) return;
        
        addMessage(text, true);
        inputField.value = '';

        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing';
        typingDiv.textContent = 'Escribiendo...';
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        setTimeout(() => {
            messagesDiv.removeChild(typingDiv);
            const respuesta = getBotResponse(text);
            addMessage(respuesta, false);
        }, 1500);
    };

    sendBtn.addEventListener('click', handleSend);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
};

// Ejecutar inmediatamente ya que el script está al final del body
initChatbot();
