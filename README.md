# Raíces Digitales: Inteligencia Agrícola y Comercio Local

Raíces Digitales es una plataforma tecnológica diseñada para revitalizar la agricultura en la zona chinampera de Xochimilco. Combina ingeniería financiera, modelos agronómicos avanzados e inteligencia artificial para empoderar a los productores locales y conectar sus cosechas directamente con el consumidor final.

---

## Arquitectura Técnica del Sistema

El proyecto está diseñado bajo un modelo de **Arquitectura Multicapa**, separando la lógica de presentación, la lógica de negocio y el acceso a datos para garantizar la integridad y seguridad de la información.

### 1. Capa de Presentación (Frontend)
Diseñada para ser ligera y altamente interactiva, utilizando tecnologías estándar para asegurar compatibilidad.
- **Vistas HTML5:** Estructura semántica organizada por módulos de usuario.
- **Estilos CSS3 (Vanilla):** Sistema de diseño basado en variables para una identidad visual coherente.
- **JavaScript (Client-Side):** Gestión de estados, peticiones AJAX y visualización de datos dinámica.

### 2. Capa de Negocio (Backend)
Construida sobre Python y Flask, actúa como el motor inteligente del sistema.
- **Controlador Principal (`app.py`):** Gestión de rutas, sesiones y validación de peticiones API.
- **Módulos de Inteligencia Especializada:** Procesamiento de fórmulas matemáticas y lógica de diagnóstico.

### 3. Capa de Persistencia y Datos (Database)
- **Motor MySQL:** Base de datos relacional para la gestión de transacciones e inventario.
- **Abstracción de Datos (`bd.py`):** Centralización de operaciones SQL seguras.

---

## Estructura Detallada de Directorios

A continuación se detalla la organización de todos los archivos y componentes del sistema:

```text
PP-Raices-Digitales-UNRC/
├── src/                        # CAPA DE BACKEND (Lógica y Modelos)
│   ├── ia/                     # Inteligencia Artificial
│   │   └── bot.py              # Lógica del Asistente Virtual (Chatbot)
│   ├── app.py                  # Controlador Central (Rutas Flask)
│   ├── bd.py                   # Gestión de Base de Datos y Seguridad
│   ├── agronomia.py            # Algoritmos de Diagnóstico de Suelo
│   ├── contabiliad.py          # Análisis Financiero y ROI
│   ├── probabilidad.py         # Cálculo de Riesgos Bayesianos
│   └── integral.py             # Cálculos de Acumulación Hídrica
├── vistas/                     # CAPA DE PRESENTACIÓN (Interfaces HTML)
│   ├── agricola/               # Vistas del Productor
│   │   ├── productor_dashboard.html   # Panel de control principal
│   │   ├── productor_inventario.html  # Gestión de lotes y stock
│   │   ├── productor_cosechas.html    # Registro de siembra y publicación
│   │   ├── productor_analiticas.html  # Visualización de datos y ROI
│   │   └── productor_ajustes.html     # Perfil y configuración de terreno
│   ├── Usuario/                # Vistas del Cliente
│   │   ├── cliente_tienda.html        # Catálogo de productos publicados
│   │   └── cliente_style.css          # Estilos específicos de la tienda
│   └── nosotros/               # Información Institucional
├── js/                         # LÓGICA DE CLIENTE (Frontend Dinámico)
│   ├── portal.js               # Animaciones y redirección de roles
│   ├── dashboard.js            # Carga dinámica de indicadores (AJAX)
│   ├── chatbot.js              # Interacción con la IA en tiempo real
│   ├── clima.js                # Consumo de API de Open-Meteo
│   ├── analiticas.js           # Generación de gráficas con Chart.js
│   ├── alertas.js              # Sistema de notificaciones visuales
│   └── responsive.js           # Adaptabilidad para dispositivos móviles
├── css/                        # SISTEMA DE DISEÑO (Estilos Globales)
│   └── index.css               # Framework visual Blanco Hueso
├── IMG/                        # RECURSOS (Logos e Imágenes)
├── .env                        # Configuración Crítica (Credenciales)
├── index.html                  # Landing Page Principal
├── pruebas.py                  # Script de Automatización de Carga (CSV)
├── style.css                   # Estilo base del proyecto
└── requirements.txt            # Dependencias de Python
```

---

## Justificación y Aplicación de Modelos Matemáticos

### 1. Ingeniería Financiera: Estabilidad y Rentabilidad
- **Retorno de Inversión (ROI):** Permite comparar la rentabilidad entre cultivos, asegurando beneficio económico real.
- **Punto de Equilibrio (PEF):** Identifica el volumen de ventas necesario para cubrir costos operativos.

### 2. Estadística Inferencial: Mitigación de Riesgos
- **Teorema de Bayes:** Actualiza la probabilidad de éxito de una cosecha basada en evidencia climática dinámica.

### 3. Cálculo Integral: Modelado de Fenómenos Continuos
- **Acumulación Hídrica:** Calcula el volumen total de agua recibido para optimizar el riego.
- **Modelado de Biomasa:** Identifica el punto de maduración óptima para maximizar la calidad del producto.

### 4. Modelos Agronómicos Especializados
- **Índice de Estrés Salino (IES):** Traduce la conductividad eléctrica del agua en un impacto económico directo de pérdida de rendimiento.

---

## Relevancia en Xochimilco: Un Enfoque Funcional

1.  **Resiliencia Hídrica:** Alerta sobre variaciones de salinidad y pH críticas para la producción local.
2.  **Sustentabilidad Económica:** Fomenta precios justos mediante la eliminación de intermediarios.
3.  **Digitalización del Campo:** Moderniza la gestión de las chinampas tradicionales para las nuevas generaciones.

---

## Tecnologías y Configuración
- **Backend:** Python / Flask.
- **Base de Datos:** MySQL.
- **Análisis de Datos:** Pandas.
- **Seguridad:** Werkzeug Hashing.

---
*Este proyecto es el resultado del esfuerzo por integrar la tecnología con las raíces agrícolas de la Ciudad de México. Universidad Nacional Rosario Castellanos - 2026.*