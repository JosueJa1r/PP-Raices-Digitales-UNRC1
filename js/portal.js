// Configuración de la URL de la API según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : '';

let globalCategories = [];

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/categorias`);
        globalCategories = await response.json();
    } catch (error) {
        console.error('Error al cargar categorías:', error);
    }
}

// Cargar categorías al inicio
loadCategories();

function addSeedRow() {
    const list = document.getElementById('seeds-list');
    const rowId = Date.now();
    const row = document.createElement('div');
    row.className = 'seed-row';
    row.id = `row-${rowId}`;
    
    let categoryOptions = '<option value="" disabled selected>Categoría...</option>';
    globalCategories.forEach(cat => {
        categoryOptions += `<option value="${cat.Id_Categoria}">${cat.Nombre_Categoria}</option>`;
    });

    row.innerHTML = `
        <select class="seed-category" onchange="updateSeedsList(${rowId}, this.value)" required>
            ${categoryOptions}
        </select>
        <select class="seed-select" name="seed_id" required>
            <option value="" disabled selected>Semilla...</option>
        </select>
        <input type="number" class="seed-qty" placeholder="Cant." required>
        <button type="button" class="btn-remove-seed" onclick="removeSeedRow(${rowId})" title="Eliminar semilla">
            &times;
        </button>
    `;
    list.appendChild(row);
}

function removeSeedRow(id) {
    document.getElementById(`row-${id}`).remove();
}

async function updateSeedsList(rowId, categoryId) {
    const row = document.getElementById(`row-${rowId}`);
    const seedSelect = row.querySelector('.seed-select');
    seedSelect.innerHTML = '<option value="" disabled selected>Cargando...</option>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/semillas_por_categoria?id_categoria=${categoryId}`);
        const seeds = await response.json();
        
        seedSelect.innerHTML = '<option value="" disabled selected>Seleccione semilla...</option>';
        seeds.forEach(s => {
            seedSelect.innerHTML += `<option value="${s.Id_Semilla}">${s.Nombre_Semilla}</option>`;
        });
    } catch (error) {
        console.error('Error al cargar semillas:', error);
        seedSelect.innerHTML = '<option value="" disabled selected>Error</option>';
    }
}

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
        
        // Recolectar semillas dinámicas
        const seeds = [];
        const seedRows = document.querySelectorAll('.seed-row');
        seedRows.forEach(row => {
            const id_semilla = row.querySelector('.seed-select').value;
            const cantidad = row.querySelector('.seed-qty').value;
            if (id_semilla && cantidad) {
                seeds.push({ id_semilla, cantidad });
            }
        });
        data.semillas = seeds;
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/register/productor`, {
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
            const response = await fetch(`${API_BASE_URL}/api/login/productor`, {
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