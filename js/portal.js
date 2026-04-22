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