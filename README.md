# Raíces Digitales: Inteligencia Agrícola, Comercio Local y Viabilidad de Nube

Raíces Digitales es una plataforma tecnológica e interactiva diseñada específicamente para revitalizar, digitalizar y potenciar la agricultura tradicional en las Chinampas de Xochimilco. Mediante el uso de algoritmos matemáticos avanzados, modelos agronómicos, analíticas de mercado interactivos e inteligencia artificial generativa, el sistema empodera a los productores chinamperos (productores), da soporte científico a los estudiantes (monitoreo ambiental) y conecta de manera directa a los consumidores con alimentos frescos libres de intermediación abusiva.

---

## Arquitectura Técnica del Sistema

El sistema implementa una Arquitectura Multicapa acoplada mediante una API RESTful que desacopla la presentación de la lógica de negocio y persistencia.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE PRESENTACIÓN (Frontend)                 │
│              HTML5 Semántico + CSS3 Vanilla + JavaScript ES6           │
└───────────────────┬─────────────────────────────────▲──────────────────┘
                    │ Peticiones AJAX (fetch)         │ Respuestas JSON
┌───────────────────▼─────────────────────────────────┴──────────────────┐
│                        CAPA DE NEGOCIO (Backend)                       │
│                     Flask Web Server + Python 3.10                     │
│  ┌───────────────────────┬─────────────────────────┬────────────────┐  │
│  │   agronomia.py        │     contabilidad.py     │ probabilidad.py│  │
│  │   (Estrés Salino)     │      (Finanzas/ROI)     │  (Riesgo Bayes)│  │
│  └───────────────────────┴─────────────────────────┴────────────────┘  │
└───────────────────┬─────────────────────────────────▲──────────────────┘
                    │ SQL Queries (Conexión Segura)   │ Tuple/Dict Sets
┌───────────────────▼─────────────────────────────────┴──────────────────┐
│                         CAPA DE PERSISTENCIA (Data)                    │
│                      Motor de Base de Datos MySQL                      │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Capa de Presentación (Frontend)
Desarrollada bajo estándares modernos, prioriza un diseño web responsivo, limpio y estéticamente premium que evoca la identidad ecológica de los canales de Xochimilco.
*   **Vistas HTML5 Semánticas:** Estructura modular independiente para Productores, Clientes e Investigadores.
*   **CSS3 Vanilla:** Sistema de variables HSL unificado, con efectos de desenfoque de fondo (glassmorphism), transiciones animadas y un modo oscuro con colores orgánicos verdes y tierra.
*   **JavaScript ES6:** Manejo dinámico del DOM, llamadas asíncronas HTTP, y renderizado de gráficos avanzados con Chart.js.

### 2. Capa de Negocio (Backend)
Construida en Python sobre la microestructura Flask. Administra el enrutamiento del sistema, la persistencia de sesiones seguras mediante hashing criptográfico y encapsula los cálculos científicos del sistema.
*   **`src/app.py`:** Controlador principal de endpoints RESTful.
*   **`src/ia/bot.py`:** Módulo integrador de la API de Gemini que permite una IA conversacional contextualizada en las necesidades agrícolas específicas de cada productor y lote.

### 3. Capa de Datos (Database)
Instancia de base de datos MySQL relacional con soporte transaccional InnoDB que garantiza consistencia ácida (ACID) y relaciones seguras de integridad referencial.
*   **`src/bd.py`:** Capa de acceso a datos que sanitiza entradas SQL previniendo ataques de inyección y gestiona el pool de conexiones activas.

---

## Estructura Detallada del Proyecto

```text
PP-Raices-Digitales-UNRC/
├── src/                        # CAPA DE BACKEND (Lógica y Modelos)
│   ├── ia/                     # Asistente Inteligente (LLM)
│   │   └── bot.py              # Lógica del chatbot con IA
│   ├── app.py                  # Controlador Principal (Rutas Flask & Middleware)
│   ├── bd.py                   # Consultas Seguras a Base de Datos
│   ├── agronomia.py            # Algoritmo de Índice de Estrés Salino (IES)
│   ├── contabilidad.py         # Análisis Financiero Avanzado (ROI y PEF)
│   ├── probabilidad.py         # Modelo Bayesiano de Riesgo de Germinación
│   └── integral.py             # Modelado de Acumulación Hídrica y Biomasa
├── vistas/                     # CAPA DE PRESENTACIÓN (Interfaces HTML5)
│   ├── agricola/               # Módulo del Productor Chinampero
│   │   ├── productor_dashboard.html   # Resumen de KPIs y clima
│   │   ├── productor_inventario.html  # Gestión de insumos y stock
│   │   ├── productor_cosechas.html    # Ciclos de cultivo (Pre-Cosecha a Venta)
│   │   ├── productor_analiticas.html  # Reportes de ROI y tendencias
│   │   └── productor_ajustes.html     # Configuración de perfil y terreno
│   ├── Usuario/                # Módulo de Comercio Local (Cliente)
│   │   ├── cliente_tienda.html        # Ecommerce de hortalizas locales
│   │   └── cliente_style.css          # Estilos visuales de la tienda
│   └── nosotros/               # Información Institucional
├── js/                         # LÓGICA DE CLIENTE (Frontend Dinámico)
│   ├── portal.js               # Control de accesos y formularios de login
│   ├── dashboard.js            # Consumo y render de KPIs en dashboard
│   ├── chatbot.js              # Interfaz de chat flotante para RaícesBot
│   ├── clima.js                # Integración con API de Clima (Open-Meteo)
│   ├── analiticas.js           # Renderizado de gráficas financieras (Chart.js)
│   ├── alertas.js              # Notificaciones visuales tipo Toast
│   └── responsive.js           # Adaptabilidad de navegación móvil
├── css/                        # SISTEMA DE DISEÑO (Estilos Globales)
│   └── index.css               # Estilo visual de la marca y portal
├── IMG/                        # Recursos Gráficos
├── .env                        # Variables de Entorno (Credenciales Críticas)
├── index.html                  # Landing Page y Portal de Acceso Principal
├── raices_digitales_setup.sql  # Esquema Relacional de Base de Datos
├── requirements.txt            # Dependencias de Python
└── style.css                   # Hoja de estilos generales compartidos
```

---

## Justificación y Aplicación de Modelos Matemáticos

Para asegurar la rigurosidad científica y financiera, Raíces Digitales ejecuta modelos matemáticos en tiempo real basados en los datos del campo y del monitoreo ambiental:

### 1. Modelo de Costos Reales y Retorno de Inversión (ROI)
Cada lote sembrado calcula dinámicamente su costo real de producción, desglosando insumos y gastos fijos asociados al tiempo del ciclo:

$$\text{Costo Real} = \text{Costo Semilla} + (\text{Mano de Obra Diaria} \times t_{\text{producción}}) + \text{Costos Herramientas} + \text{Mantenimiento Fijo}$$

En el código python (`src/app.py`), esta fórmula se ejecuta como:
```python
tiempo_prod = cos.get('Tiempo_Produccion') or 90
costo_semilla = calcular_costo_siembra_realista(precio_costal, area_m2)
costo_real = costo_semilla + (350.0 * tiempo_prod) + 400.0 + 900.0
```
Donde:
*   **Costo de Semilla:** Se calcula en función del área cultivada ($m^2$), la densidad óptima de siembra y el valor proporcional del costal de semillas de la base de datos.
*   **Mano de Obra Fija:** $\$350.00$ MXN diarios asignados a jornales multiplicados por los días requeridos para que la planta madure ($t_{\text{producción}}$).
*   **Herramientas y Desgaste:** Costo amortizado fijo de $\$400.00$ MXN por ciclo.
*   **Mantenimiento del Lote:** Cuota fija de $\$900.00$ MXN por concepto de riego tradicional, control orgánico de plagas y limpieza del canal.

A partir del costo real, se calcula el **ROI Proyectado** una vez que se simula o registra el valor de venta del lote:

$$\text{ROI} = \left( \frac{\text{Valor de Venta} - \text{Costo Real}}{\text{Costo Real}} \right) \times 100$$

### 2. Probabilidad Bayesiana para Éxito de Germinación
La probabilidad de pérdida o germinación exitosa se ajusta a partir de los datos históricos chinamperos modificados por variables ambientales actuales de pH y salinidad del agua tomadas del monitoreo semanal:

$$P(\text{Germinación}) = P(\text{Base}) \times f(\text{pH}) \times f(\text{Salinidad})$$

*   **Factor pH ($f(\text{pH})$):** Evalúa la desviación del pH medido con respecto al pH óptimo de la planta. Desviaciones menores a $0.5$ unidades mantienen el factor en $1.0$. Desviaciones mayores penalizan linealmente el éxito de germinación.
*   **Factor Salinidad ($f(\text{Salinidad})$):** La conductividad eléctrica superior a $1.5\text{ dS/m}$ reduce de forma exponencial la absorción de nutrientes, penalizando la viabilidad del cultivo.

### 3. Modelado de Merma Económica y Riesgo de Insuficiencia
Utilizando una **Distribución Binomial**, el sistema estima la probabilidad acumulada de que la germinación real caiga por debajo del umbral mínimo requerido para cumplir un pedido comercial:

$$P(X < k) = \sum_{x=0}^{k-1} \binom{n}{x} p^x (1-p)^{n-x}$$

Donde $n$ es la cantidad de semillas proyectadas, $k$ es el pedido mínimo y $p$ es la probabilidad de germinación ajustada por Bayes. Esto permite generar un indicador visual del **Riesgo de Desabasto** antes de cosechar el lote.

---

## Costos en la Nube, Viabilidad y Payback (Retorno de Inversión)

Para garantizar que Raíces Digitales sea un proyecto viable para la comunidad, se ha diseñado una estructura de costos operativos de infraestructura optimizados en la nube:

### 1. Costo Operativo de Infraestructura Mensual
El sistema está diseñado sobre plataformas en la nube de pago por uso y capas de desarrollo optimizadas:

| Componente | Proveedor / Servicio | Configuración de Servidor | Costo Estimado (Mensual) |
| :--- | :--- | :--- | :--- |
| **Base de Datos** | Aiven Cloud MySQL | Plan Startup (1 CPU, 1GB RAM, 10GB SSD) | $320.00 MXN ($19 USD) |
| **Backend API** | Render Cloud | Instancia Web Flask (0.5 CPU, 512MB RAM) | $250.00 MXN ($15 USD) |
| **Frontend** | Vercel | CDN Edge Distributions & Static Hosting | $340.00 MXN ($20 USD) |
| **API Asistente Inteligente** | Gemini Cloud API | Pago por consumo de tokens (~20,000 consultas) | $200.00 MXN ($10 USD) |
| **Dominio y Certificados** | GoDaddy / Let's Encrypt | Dominio `.mx` con cifrado SSL automático | $50.00 MXN ($2.5 USD) |
| **Mantenimiento Técnico** | Soporte Remoto | Actualizaciones mensuales y respaldos | $2,000.00 MXN |
| **TOTAL MENSUAL** | | | **$3,160.00 MXN** |

> [!NOTE]
> Dado que la base de datos MySQL en Aiven Cloud y el hosting de Vercel soportan múltiples accesos recurrentes, el costo mensual es plano para la comunidad. Si hay 200 productores activos, el costo mensual de infraestructura por chinampero es de tan solo **$15.80 MXN**.

### 2. Periodo de Recuperación (Payback Period)
Asumiendo un costo de desarrollo inicial de **$120,000.00 MXN** (diseño UI/UX, maquetación, conexión con base de datos, modelos matemáticos e inteligencia artificial conversacional), se evalúan dos vías de retorno financiero sustentable:

*   **Modelo A: Cuota de Cooperativa Agrícola (Suscripción)**
    *   Suscripción mensual de **$25.00 MXN** por productor (incluye acceso completo a analíticas, RaícesBot y pasarela de venta).
    *   Con **500 productores activos**, se recaudan $\$12,500.00$ MXN mensuales.
    *   Restando el costo operativo mensual ($\$3,160.00$ MXN), se genera un flujo libre de efectivo neto de **$9,340.00 MXN mensuales**.
    *   **Payback Period:** **13 meses** para recuperar la inversión total del desarrollo.
*   **Modelo B: Comisión por Intermediación Justa (2% por venta)**
    *   Uso de la aplicación 100% gratuito. Se cobra una tasa de servicio del **2%** por cada transacción exitosa realizada por los clientes finales a través del catálogo web.
    *   Con **200 productores activos** vendiendo un promedio de $\$3,000.00$ MXN mensuales cada uno, el volumen de comercio local total es de $\$600,000.00$ MXN mensuales.
    *   La comisión del 2% genera un ingreso bruto de $\$12,000.00$ MXN mensuales.
    *   Restando el costo operativo, el beneficio neto para la plataforma es de **$8,840.00 MXN mensuales**.
    *   **Payback Period:** **14 meses** para el retorno completo de la inversión.

---

## Plan de Escalabilidad y Crecimiento

El diseño desacoplado de Raíces Digitales permite la escalabilidad del sistema a nivel arquitectónico y operativo conforme crece el volumen de usuarios activos:

```
                  ┌───────────────────────────────┐
                  │   DNS Anycast (Cloudflare)    │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │ Balanceador de Cargas (NGINX) │
                  └───────┬───────────────┬───────┘
                          │               │
       ┌──────────────────▼──┐         ┌──▼──────────────────┐
       │ Backend Instancia 1 │         │ Backend Instancia 2 │
       │     (Flask API)     │         │     (Flask API)     │
       └──────────┬──────────┘         └──────────┬──────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │    Capa Caché Redis (RAM)     │
                  └───────────────┬───────────────┘
                                  │
        ┌─────────────────────────┴─────────────────────────┐
        │                                                   │
┌───────▼─────────────────┐                       ┌─────────▼───────────────┐
│ BD Principal (Escritura)│                       │ BD Réplica (Lectura)    │
│    Aiven MySQL Primary  │                       │   Aiven MySQL Replica   │
└─────────────────────────┘                       └─────────────────────────┘
```

### 1. Escalabilidad de la Arquitectura de Software
*   **Migración a Contenedores Docker e Integración con Kubernetes:** Permite levantar réplicas del servidor Flask automáticamente en segundos ante picos de demanda estacionales (por ejemplo, durante la temporada alta de ventas de Flor de Cempasúchil en Otoño).
*   **Caché en Memoria con Redis:** Para evitar consultas repetitivas a la base de datos MySQL por parte de miles de clientes consultando el catálogo de la tienda, se implementará una base de caché Redis. Los productos listos para la venta se guardan en caché de memoria, acelerando la respuesta del catálogo a menos de $15\text{ ms}$ y reduciendo la carga de lectura en la base de datos hasta en un 80%.
*   **Réplicas de Lectura en MySQL (Read Replicas):** Al escalar la base de datos a un esquema de alta disponibilidad en Aiven Cloud, se separan las operaciones: un servidor MySQL primario se encarga de las escrituras de inventario y monitoreo de los agricultores, mientras que réplicas de lectura secundarias atienden las miles de consultas concurrentes de los compradores de la tienda.

### 2. Escalabilidad del Modelo Operativo y Regional
*   **Estructura Multichinampa:** La base de datos actual posee un diseño relacional que permite segmentar y catalogar datos de suelo y rendimiento por región. Esto facilita llevar la plataforma a otras zonas lacustres o agrícolas urbanas de la Ciudad de México (como Tláhuac o Milpa Alta) de manera inmediata.
*   **Modularidad de Algoritmos:** Las funciones de cálculo financiero y agronómico están desacopladas en módulos puros de Python. Si se introduce un nuevo sensor de calidad de suelo (conductividad térmica, nitrógeno o potasio), solo es necesario escribir una nueva función en `src/agronomia.py` e integrarla a la base de datos sin alterar la interfaz de usuario ni las rutas de venta.

---

## Requisitos e Instalación

Para ejecutar Raíces Digitales localmente en entorno de desarrollo, sigue estos pasos:

1.  **Clona el repositorio**
    ```bash
    git clone https://github.com/JosueJa1r/PP-Raices-Digitales-UNRC.git
    cd PP-Raices-Digitales-UNRC
    ```

2.  **Crea y activa un entorno virtual de Python**
    ```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Instala las dependencias necesarias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno**
    Crea un archivo llamado `.env` en la raíz del proyecto y configura tus credenciales de base de datos MySQL y la llave API del bot de inteligencia artificial:
    ```ini
    MYSQL_HOST=tu-host-mysql.com
    MYSQL_PORT=3306
    MYSQL_USER=tu-usuario
    MYSQL_PASSWORD=tu-contraseña
    MYSQL_DATABASE=raices_digitales
    BOT_CHAT=tu-api-key-gemini
    ```

5.  **Inicia el servidor Flask**
    ```bash
    python -m src.app
    ```
    El servidor backend estará disponible en `http://127.0.0.1:5000`. Puedes abrir los archivos HTML locales en un navegador (o levantando un servidor local en el puerto `5501` para evitar bloqueos CORS) para interactuar con la plataforma completa.

---

*Este desarrollo tecnológico es fruto del compromiso académico por preservar las tradiciones agrícolas de la Ciudad de México mediante la innovación digital. Comunidad LCDN UNRC - 2026.*