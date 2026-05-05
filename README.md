## Fórmulas Matemáticas y Financieras Aplicadas

A continuación se detallan las fórmulas y modelos matemáticos identificados y aplicados en el análisis y funcionamiento de la plataforma "Raíces Digitales":

### 1. Contabilidad Financiera
El módulo del panel de producción requiere modelos de contabilidad para el cálculo de ganancias, control de inventario y estimaciones de valor neto para el catálogo de la tienda.
*   **Cálculo de Utilidad Neta (Net Profit):**
    `Utilidad Neta = Ingresos Totales - Costos Totales (Insumos + Operativos)`
    *Aplicación:* Utilizado para mostrar el "Valor Estimado Neto" de las cosechas activas y determinar márgenes en la interfaz del cliente.
*   **Retorno de Inversión (ROI):**
    `ROI = [(Ganancia de Cosecha - Costo de Siembra) / Costo de Siembra] * 100`
    *Aplicación:* Permite a los productores evaluar la rentabilidad de sembrar ciertas semillas (ej. Cempasúchil en temporada) frente a otras hortalizas.
*   **Punto de Equilibrio Financiero (PEF):**
    `PEF = Costos Fijos / (Precio de Venta por Unidad - Costo Variable por Unidad)`
    *Aplicación:* Permite al productor conocer exactamente cuántas unidades (kilos, macetas, manojos) necesita vender en la tienda para cubrir su inversión inicial y costos operativos, evitando pérdidas.
*   **Cálculo de Merma Económica Proyectada (ME):**
    `ME = (Volumen Esperado * Probabilidad de Pérdida) * Precio de Venta Estimado`
    *Aplicación:* Integra la estadística probabilística con el análisis financiero para cuantificar monetariamente el riesgo por condiciones climáticas adversas o plagas en el panel de analíticas.

### 2. Probabilidad y Estadística
Mediante la integración de la API del clima (Open-Meteo) y el análisis de datos agrícolas, se pueden utilizar modelos probabilísticos para la predicción y mitigación de riesgos.
*   **Teorema de Bayes (Probabilidad Condicional):** VERIFICAR 
    `P(Éxito | Clima) = [P(Clima | Éxito) * P(Éxito)] / P(Clima)`
    *Aplicación:* El *RaícesBot IA* y el sistema de analíticas evalúan la probabilidad de que una cosecha sea exitosa dado un pronóstico de lluvias atípicas, heladas o sequías.
*   **Distribución Probabilística de Pérdidas:**
    Uso de distribuciones para estimar la merma o pérdida de producto basada en el historial probabilístico del productor, afectando el stock proyectado.

### 3. Cálculo Integral
Se emplea el cálculo continuo para modelos predictivos de acumulación, ya sea de recursos hídricos, estimación de crecimiento de plantas o análisis de ingresos continuos.
*   **Acumulación de Precipitación y Riego:**
    $P_{total} = \int_{0}^{T} p(t) dt$
    *Donde:* $p(t)$ es la función de tasa de precipitación (mm/día) a lo largo del tiempo $t$.
    *Aplicación:* Calcula el volumen total de agua recibida por una hectárea en Xochimilco durante el ciclo de siembra.
*   **Volumen de Biomasa (Crecimiento del Cultivo):**
    $V = \int_{t_0}^{t_f} r(t) dt$
    *Donde:* $r(t)$ representa la tasa instantánea de crecimiento diario dependiente de nutrientes y el clima.
    *Aplicación:* Ayuda a estimar las fechas ideales de cosecha en el sistema, prediciendo el punto de volumen óptimo antes del declive de calidad del producto fresco.

### 4. Modelos Agronómicos Especializados
Para adaptar la plataforma a las particularidades agrícolas de la región (como la zona chinampera de Xochimilco), se incorporan modelos de estrés ambiental.
*   **Índice de Estrés Salino (IES):**
    `IES = (CE - CE_umbral) * b`
    *Donde:* $CE$ es la Conductividad Eléctrica del suelo/agua observada, $CE_{umbral}$ es la tolerancia máxima del cultivo sin pérdida, y $b$ es la pendiente de reducción de rendimiento.
    *Aplicación:* Dado que la calidad del agua varía, esta fórmula ayuda a pronosticar la reducción porcentual del volumen de cosechas sensibles y enviar alertas tempranas al Productor.