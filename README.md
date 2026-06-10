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
*   **Vistas HTML5 Semánticas:** Estructura modular independiente para Productores, Clientes, Estudiantes de Monitoreo e Investigadores.
*   **CSS3 Vanilla y Neobrutalismo:** Sistema de variables HSL unificado para la tienda y paneles, junto con un diseño neobrutalista (bordes negros gruesos y sombras sólidas) con una navegación compacta por pestañas para las herramientas estudiantiles.
*   **JavaScript ES6:** Manejo dinámico del DOM (interactividad de pestañas y carga de clima por API Open-Meteo), llamadas asíncronas HTTP (fetch), y renderizado de gráficos avanzados con Chart.js optimizados para redimensionamiento en vistas ocultas.

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
│   ├── Usuario/                # Módulo de Comercio Local y Estudiantil
│   │   ├── cliente_tienda.html        # Ecommerce de hortalizas locales
│   │   ├── cliente_style.css          # Estilos visuales de la tienda
│   │   └── estudiante_dashboard.html  # Panel de monitoreo estudiantil y herramientas técnicas
│   └── nosotros/               # Información Institucional
├── js/                         # LÓGICA DE CLIENTE (Frontend Dinámico)
│   ├── portal.js               # Control de accesos y formularios de login
│   ├── dashboard.js            # Consumo y render de KPIs en dashboard
│   ├── chatbot.js              # Interfaz de chat flotante para RaícesBot
│   ├── clima.js                # Integración con API de Clima (Open-Meteo)
│   ├── analiticas.js           # Renderizado de gráficas financieras (Chart.js)
│   ├── estudiante.js           # Lógica del panel estudiantil, recomendador, regresión y Riemann
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

### 4. Volumen de Acumulación Hídrica y Biomasa (Cálculo Integral - Suma de Riemann)
El sistema aproxima integrales definidas en tiempo real utilizando la Suma de Riemann izquierda para cuantificar variables acumulativas a partir de tasas de variación diarias (con un intervalo de tiempo fijo $\Delta t = 1$ día):

$$A \approx \sum_{i=1}^{n} f(t_i) \Delta t = \sum_{i=1}^{n} f(t_i) \cdot 1$$

*   **Precipitación Acumulada:** Integra la tasa diaria de lluvia en mm o $L/m^2$ para calcular el riego pasivo acumulado que recibió la chinampa a lo largo del tiempo:
    $$V_{\text{agua}} = \sum_{i=1}^{n} P(t_i) \quad [\text{L/m}^2]$$
*   **Acumulación de Biomasa:** Integra la tasa diaria de crecimiento de biomasa ($g/\text{día}$) de las plantas para proyectar el peso / biomasa neta total obtenida en el ciclo:
    $$M_{\text{biomasa}} = \sum_{i=1}^{n} B(t_i) \quad [\text{g}]$$

En el backend de Python (`src/integral.py`), estas sumas discretas se calculan en las funciones:
- `integral_acumulacion_precipitacion(tasa_lluvia_diaria)` $\rightarrow$ Aproxima el volumen total de agua recibida.
- `integral_volumen_biomasa(tasa_crecimiento_diario)` $\rightarrow$ Aproxima el peso neto acumulado de la planta.

---

## Costos en la Nube, Viabilidad y Payback (Retorno de Inversión)

Para garantizar que Raíces Digitales sea un proyecto viable, escalable y comercialmente transferible, se ha diseñado una estructura de costos operativos de infraestructura en la nube (comparando **Amazon Web Services (AWS)** y **Oracle Cloud Infrastructure (OCI)**) junto con la valorización del desarrollo profesional.

### 1. Costo Operativo de Infraestructura Mensual (Producción)

A continuación se detallan las dos alternativas de arquitectura de nube comercial:

#### Alternativa A: Amazon Web Services (AWS)
| Componente | Servicio AWS | Configuración de Servidor | Costo Estimado (Mensual) |
| :--- | :--- | :--- | :--- |
| **Base de Datos** | Amazon RDS for MySQL | Instancia `db.t4g.micro` (2 vCPUs, 1GB RAM, 20GB SSD gp3) | $340.00 MXN ($20 USD) |
| **Backend API** | AWS App Runner / ECS | Contenedor de microservicio Flask (0.5 vCPU, 1GB RAM) | $255.00 MXN ($15 USD) |
| **Frontend** | AWS Amplify / S3 + CloudFront | Hosting estático y distribución de CDN Edge | $85.00 MXN ($5 USD) |
| **Asistente IA** | Gemini API | Consumo promedio de tokens para asistente conversacional | $170.00 MXN ($10 USD) |
| **DNS & Seguridad** | AWS Route 53 + Shield | Resolución de dominio y protección básica contra DDoS | $34.00 MXN ($2 USD) |
| **Soporte & Mantenimiento** | Soporte Remoto Técnico | Actualizaciones y backups automatizados (S3) | $2,000.00 MXN |
| **TOTAL MENSUAL AWS** | | | **$2,884.00 MXN** |

#### Alternativa B: Oracle Cloud Infrastructure (OCI)
| Componente | Servicio OCI | Configuración de Servidor | Costo Estimado (Mensual) |
| :--- | :--- | :--- | :--- |
| **Base de Datos** | OCI MySQL Database Service | Forma mínima dedicada (1 OCPU, 8GB RAM, 50GB Block Volume) | $425.00 MXN ($25 USD) |
| **Backend API** | OCI Compute Instance | Instancia Standard.E4.Flex (1 OCPU, 2GB RAM Linux) | $204.00 MXN ($12 USD) |
| **Frontend** | OCI Object Storage + CDN | Almacenamiento de cubos y distribución de borde WAF | $51.00 MXN ($3 USD) |
| **Asistente IA** | Gemini API | Integración externa por API | $170.00 MXN ($10 USD) |
| **DNS & Seguridad** | OCI DNS & WAF | Administración de dominio y firewall de aplicaciones | $34.00 MXN ($2 USD) |
| **Soporte & Mantenimiento** | Soporte Remoto Técnico | Actualizaciones y backups de bloque | $2,000.00 MXN |
| **TOTAL MENSUAL OCI** | | | **$2,884.00 MXN** |

> [!NOTE]
> Ambas opciones de nube profesional son muy similares en costo, rondando los **$2,884.00 MXN mensuales** (con el soporte técnico incluido). A nivel de infraestructura pura de nube, el costo es de apenas **$884.00 MXN mensuales**, lo que hace que el sistema sea extremadamente ligero y económicamente viable.

---

### 2. Valor de Adquisición y Costo de Desarrollo del Proyecto (Venta del Software)

Si una cooperativa agrícola, una entidad gubernamental (como la alcaldía de Xochimilco) o un inversor privado desea comprar el proyecto completo, se ha calculado una valorización profesional basada en horas de desarrollo y la participación de los **cuatro integrantes del equipo de proyecto** y el **desarrollador líder**:

*   **Mano de Obra del Desarrollador Líder (Ingeniería de Software & DevOps):**
    *   3 meses de trabajo dedicados al diseño de la base de datos relacional MySQL, estructuración del backend API REST con Flask, lógica del chatbot con el SDK de Gemini, codificación matemática de los modelos y despliegue local/nube.
    *   **Costo:** $30,000.00 MXN mensuales $\times$ 3 meses = **$90,000.00 MXN**.
*   **Mano de Obra de los 4 Integrantes del Equipo (Gestión, Investigación Agronómica y QA):**
    *   Trabajo multidisciplinario enfocado en:
        1. *Investigación Agronómica:* Formulación matemática del Índice de Estrés Salino (IES) y recolección de pH/Salinidad óptimos de cultivos de Xochimilco.
        2. *Matemáticas y Probabilidad:* Modelado Bayesiano y cálculo de riesgos de merma con distribución binomial.
        3. *Diseño y Documentación:* Estructuración de requerimientos, diagramas de flujo y bases de datos.
        4. *Aseguramiento de Calidad (QA):* Pruebas del software y validación con datos reales.
    *   **Costo:** $15,000.00 MXN mensuales por integrante $\times$ 4 integrantes $\times$ 3 meses = **$180,000.00 MXN**.
*   **VALOR DE VENTA / ADQUISICIÓN TOTAL DEL PROYECTO:**
    $$\text{Costo Total} = \text{Mano de Obra Desarrollador} + \text{Mano de Obra de Integrantes} = \$90,000 + \$180,000 = \mathbf{\$270,000.00\text{ MXN}}$$

---

### 3. Modelos de Monetización y Cálculo Integral para la Reinversión

Para garantizar el crecimiento sustentable de la plataforma (adquisición de hardware de monitoreo, sensores de suelo automatizados y optimización de servidores), se ha diseñado un modelo de reinversión basado en **Cálculo Integral**. 

Definimos que el número de productores chinamperos en la plataforma crece de forma lineal a lo largo del tiempo $t$ (medido en meses):
$$N(t) = N_0 + r \cdot t$$
Donde:
*   $N_0 = 100$ (Productores iniciales en el mes $0$).
*   $r = 15$ (Crecimiento de $15$ nuevos productores al mes).
*   $N(t) = 100 + 15t$.

Definimos los costos fijos operativos mensuales como $C_{\text{fijo}} = \$3,200.00\text{ MXN}$ (infraestructura AWS/OCI + mantenimiento). El fondo de reinversión acumulado $R(T)$ después de $T$ meses es la integral del flujo neto de efectivo $I(t)$ desde el inicio hasta el mes $T$:
$$R(T) = \int_{0}^{T} I(t) \, dt = \int_{0}^{T} \left( B(t) - C_{\text{fijo}} \right) \, dt$$
Donde $B(t)$ representa los ingresos brutos generados por el modelo de negocio.

#### Modelo A: Suscripción Mensual Fija
Se establece una cuota de cooperativa de **$25.00 MXN mensuales** por productor.
*   **Ingreso Bruto Mensual:** $B(t) = 25 \cdot N(t) = 25(100 + 15t) = 2500 + 375t\text{ MXN/mes}$.
*   **Flujo Neto Mensual:** $I(t) = B(t) - C_{\text{fijo}} = (2500 + 375t) - 3200 = 375t - 700\text{ MXN/mes}$.
*   **Punto de Equilibrio (Break-Even):** Ocurre cuando el flujo neto es cero, es decir:
    $$375t - 700 = 0 \implies t_{\text{eq}} = \frac{700}{375} \approx 1.87\text{ meses}$$
*   **Fondo de Reinversión Acumulado $R(T)$ (Integrando desde $t_{\text{eq}}$ hasta $T$):**
    $$R(T) = \int_{1.87}^{T} (375t - 700) \, dt = \left[ 187.5 t^2 - 700t \right]_{1.87}^{T}$$
*   **Proyección al Primer Año ($T = 12$ meses):**
    $$R(12) = \left( 187.5(12)^2 - 700(12) \right) - \left( 187.5(1.87)^2 - 700(1.87) \right)$$
    $$R(12) = (27,000 - 8,400) - (655.3 - 1,309) = 18,600 - (-653.7) \approx \mathbf{\$19,253.70\text{ MXN}}$$

#### Modelo B: Comisión del 2% por Transacción (Tienda Local)
El uso es gratuito para los productores, cobrando una comisión del **2% sobre cada venta** realizada por el cliente final. 
*   Asumimos un volumen promedio de venta por productor de **$3,000.00 MXN mensuales** (hortalizas, flores, etc.).
*   Esto genera una comisión de $\$3,000.00 \times 0.02 = \$60.00\text{ MXN}$ mensuales por productor activo.
*   **Ingreso Bruto Mensual:** $B(t) = 60 \cdot N(t) = 60(100 + 15t) = 6000 + 900t\text{ MXN/mes}$.
*   **Flujo Neto Mensual:** $I(t) = B(t) - C_{\text{fijo}} = (6000 + 900t) - 3200 = 2800 + 900t\text{ MXN/mes}$ (Flujo positivo desde el mes $0$).
*   **Fondo de Reinversión Acumulado $R(T)$ (Integrando desde el mes $0$ hasta $T$):**
    $$R(T) = \int_{0}^{T} (2800 + 900t) \, dt = \left[ 2800t + 450t^2 \right]_{0}^{T} = 2800T + 450T^2$$
*   **Proyección al Primer Año ($T = 12$ meses):**
    $$R(12) = 2800(12) + 450(12)^2 = 33,600 + 450(144) = 33,600 + 64,800 = \mathbf{\$98,400.00\text{ MXN}}$$

> [!TIP]
> **Comparativa y Conclusión de Reinversión:** El **Modelo B (Comisión del 2%)** es sustancialmente más lucrativo y sostenible, ya que al primer año de operación acumula un fondo de reinversión de **$98,400.00 MXN** frente a los **$19,253.70 MXN** del Modelo A, permitiendo comprar hardware de monitoreo IoT (como sensores de pH y salinidad de Arduino/Raspberry Pi) para repartirlos directamente a la comunidad chinampera.



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