# 📋 Reporte de Pendientes: Raíces Digitales

Este documento detalla el estado actual del desarrollo y las tareas críticas restantes para completar la plataforma de soporte agrícola y comercial.

---

## ✅ Módulos Completados
| Módulo | Funcionalidad | Estado |
| :--- | :--- | :--- |
| **Backend Core** | Flask API, Conexión MySQL, Variables de Entorno (.env) | 100% |
| **Dashboard Productor** | Carga dinámica de cosechas, stats de terreno y ROI. | 100% |
| **Gestión de Inventario** | Registro de insumos por agricultor, cálculo de stock crítico. | 100% |
| **Inteligencia Agrícola** | Automatización de ROI, Estrés Salino y Probabilidad Bayesiana. | 100% |
| **Explorador de Mercado** | Gráficas globales (Chart.js) y detección de tendencias. | 100% |
| **Seguridad** | Registro y Login con Hashing de contraseñas (Werkzeug). | 100% |

---

## 🛠️ Tareas Pendientes Prioritarias

### 1. Portal del Cliente (Tienda) 🛒
- **Vista de Catálogo**: Crear la interfaz donde los clientes puedan ver todos los productos publicados por los productores.
- **Carrito de Compras**: Implementar la lógica de selección y suma de productos.
- **Simulación de Pago**: Botón de "Comprar" que descuente automáticamente el stock de la tabla `inventario`.

### 2. Publicación de Productos 📢
- **Finalizar Formulario**: En `productor_cosechas.html`, conectar el formulario de "Registrar y Publicar" para que los productos terminados pasen de "En Bodega" a "En Venta".
- **Gestión de Estados**: Permitir que el productor marque un producto como "Agotado" o "En Oferta".

### 3. Seguridad y Sesiones Avanzadas 🔐
- **Implementar JWT**: Migrar la identificación actual (localStorage) a Tokens JWT para mayor seguridad en las peticiones API.
- **Protección de Rutas**: Asegurar que un productor no pueda ver o editar el inventario de otro productor mediante fuerza bruta en la URL.

### 4. Perfil y Ajustes ⚙️
- **Gestión de Terrenos**: Permitir al productor actualizar las hectáreas de su terreno y el tipo de suelo (esto afectará automáticamente el cálculo de ROI).
- **Notificaciones**: Sistema de alertas visuales cuando el IES (Índice de Estrés Salino) sea crítico para una semilla específica.

### 5. Optimización de IA (RaícesBot) 🤖
- **Contexto Agrícola**: Refinar el prompt del bot para que utilice los datos de ROI y Clima local para dar consejos más precisos.

---

## 🚀 Próximos Pasos Recomendados
1.  **Integrar el Formulario de Venta**: Permitir que el productor "ponga en el aparador" sus cosechas actuales.
2.  **Desarrollar la Vista del Cliente**: Es vital para cerrar el ciclo económico de la aplicación.
3.  **Refinar el ROI**: Sustituir el costo simulado (70%) por una entrada de datos real en el formulario de siembra.

---
> [!IMPORTANT]
> **Nota de Desarrollo**: El sistema ya es funcional en un 80% para el rol de productor. El enfoque debe girar ahora hacia el flujo de salida de mercancía (Venta y Clientes).
