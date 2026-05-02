function showForm(role) {
            document.getElementById('selection-cards').style.display = 'none';
            document.querySelector('.portal-header p').innerText = role === 'productor' ? 'Acceso Seguro para Productores' : 'Acceso para Clientes';
            document.getElementById('form-' + role + '-container').style.display = 'block';
        }
        
        function goBack() {
            document.getElementById('form-productor-container').style.display = 'none';
            document.getElementById('form-cliente-container').style.display = 'none';
            document.getElementById('selection-cards').style.display = 'flex';
            document.querySelector('.portal-header p').innerText = 'Selecciona tu perfil para continuar';
            
            // Reset to login forms
            toggleAuth('productor', 'login');
            toggleAuth('cliente', 'login');
        }
        
        function toggleAuth(role, action) {
            if (action === 'register') {
                document.getElementById('login-' + role).style.display = 'none';
                document.getElementById('register-' + role).style.display = 'block';
                document.getElementById('title-' + role).innerText = 'Registro ' + (role === 'productor' ? 'Productor' : 'Cliente');
            } else {
                document.getElementById('register-' + role).style.display = 'none';
                document.getElementById('login-' + role).style.display = 'block';
                document.getElementById('title-' + role).innerText = 'Ingreso ' + (role === 'productor' ? 'Productor' : 'Cliente');
            }
        }

// --- Integración con Backend (Productor) ---

// Manejo del Registro de Productor
const formRegisterProductor = document.getElementById('register-productor');
if (formRegisterProductor) {
    formRegisterProductor.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(formRegisterProductor);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/register/productor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                alert('¡Registro exitoso! Bienvenido ' + data.nombre);
                // Guardar en localStorage si es necesario
                localStorage.setItem('productor_id', result.id_productor);
                localStorage.setItem('productor_nombre', data.nombre);
                window.location.href = 'vistas/agricola/productor_dashboard.html';
            } else {
                alert('Error en registro: ' + (result.error || 'Intente de nuevo.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al conectar con el servidor: ' + error.message + '. Asegúrate de haber configurado las variables de entorno en Vercel.');
        }
    });
}

// Manejo del Login de Productor
const formLoginProductor = document.getElementById('login-productor');
if (formLoginProductor) {
    formLoginProductor.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(formLoginProductor);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/login/productor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Guardar datos de sesión básica
                localStorage.setItem('productor_id', result.user.Id_Productor);
                localStorage.setItem('productor_nombre', result.user.Nombre);
                window.location.href = 'vistas/agricola/productor_dashboard.html';
            } else {
                alert('Error en login: ' + (result.error || 'Credenciales inválidas.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al conectar con el servidor: ' + error.message + '. Asegúrate de haber configurado las variables de entorno en Vercel.');
        }
    });
}