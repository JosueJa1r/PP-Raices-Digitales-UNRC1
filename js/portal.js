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
        <input type="number" class="seed-qty" placeholder="Cant." required style="width: 80px;">
        <select class="seed-unit" required style="width: 100px;">
            <option value="" disabled selected>Unidad...</option>
            <option value="Kg">Kg</option>
            <option value="Manojo">Manojo</option>
            <option value="Pieza">Pieza</option>
            <option value="Gramo">Gramo</option>
            <option value="Caja">Caja</option>
        </select>
        <button type="button" class="btn-remove-seed" onclick="removeSeedRow(${rowId})" title="Eliminar cosecha">
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
    let label = 'Acceso para Clientes';
    if (role === 'productor') {
        label = 'Acceso Seguro para Productores';
    } else if (role === 'estudiante') {
        label = 'Acceso para Estudiantes de Apoyo';
    }
    document.querySelector('.portal-header p').innerText = label;
    document.getElementById('form-' + role + '-container').style.display = 'block';
}

function goBack() {
    document.getElementById('form-productor-container').style.display = 'none';
    document.getElementById('form-cliente-container').style.display = 'none';
    document.getElementById('form-estudiante-container').style.display = 'none';
    document.getElementById('selection-cards').style.display = 'flex';
    document.querySelector('.portal-header p').innerText = 'Selecciona tu perfil para continuar';
    
    // Reset to login forms
    toggleAuth('productor', 'login');
    toggleAuth('cliente', 'login');
    toggleAuth('estudiante', 'login');
}

function toggleAuth(role, action) {
    let labelRole = role === 'productor' ? 'Productor' : (role === 'cliente' ? 'Cliente' : 'Estudiante');
    if (action === 'register') {
        document.getElementById('login-' + role).style.display = 'none';
        document.getElementById('register-' + role).style.display = 'block';
        document.getElementById('title-' + role).innerText = 'Registro ' + labelRole;
    } else {
        document.getElementById('register-' + role).style.display = 'none';
        document.getElementById('login-' + role).style.display = 'block';
        document.getElementById('title-' + role).innerText = 'Ingreso ' + labelRole;
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
            const unidad = row.querySelector('.seed-unit').value;
            if (id_semilla && cantidad) {
                seeds.push({ id_semilla, cantidad, unidad });
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

// --- Integración con Backend (Estudiante) ---

// Manejo del Registro de Estudiante
const formRegisterEstudiante = document.getElementById('register-estudiante');
if (formRegisterEstudiante) {
    formRegisterEstudiante.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(formRegisterEstudiante);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/register/estudiante`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                alert('¡Registro exitoso! Bienvenido ' + data.nombre);
                localStorage.setItem('estudiante_id', result.id_estudiante);
                localStorage.setItem('estudiante_nombre', data.nombre);
                window.location.href = 'vistas/Usuario/estudiante_dashboard.html';
            } else {
                alert('Error en registro: ' + (result.error || 'Intente de nuevo.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al conectar con el servidor: ' + error.message);
        }
    });
}

// Manejo del Login de Estudiante
const formLoginEstudiante = document.getElementById('login-estudiante');
if (formLoginEstudiante) {
    formLoginEstudiante.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(formLoginEstudiante);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/login/estudiante`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                localStorage.setItem('estudiante_id', result.user.Id_Estudiante);
                localStorage.setItem('estudiante_nombre', result.user.Nombre);
                window.location.href = 'vistas/Usuario/estudiante_dashboard.html';
            } else {
                alert('Error en login: ' + (result.error || 'Credenciales inválidas.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al conectar con el servidor: ' + error.message);
        }
    });
}