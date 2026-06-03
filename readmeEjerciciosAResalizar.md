# Ejercicios de Probabilidad Aplicada - Raíces Digitales

Este documento contiene un ejercicio resuelto detalladamente y dos ejercicios para resolver en el cuaderno, enfocados en la aplicación de modelos matemáticos (Teorema de Bayes y Distribución Binomial) en el contexto de la agricultura chinampera de Xochimilco.

---

## Ejercicio Explicado: Teorema de Bayes en las Chinampas

### Contexto del Problema
En Xochimilco, un productor de lechugas sabe que históricamente la probabilidad general de que sus semillas germinen con éxito es del 85% ($P(G) = 0.85$). 
Los estudiantes de la Universidad Rosario Castellanos realizan monitoreos de pH en el canal de agua. Se sabe que:
* Si la semilla germina con éxito, el pH del agua se mide como Óptimo (entre 6.2 y 6.8) en el 90% de los casos ($P(\text{Óptimo} | G) = 0.90$).
* Si la semilla falla en su germinación, el pH se reporta como Óptimo únicamente el 30% de las veces debido a anomalías ácidas en el fango ($P(\text{Óptimo} | F) = 0.30$).

Hoy, un estudiante mide el pH en el canal y reporta que el agua está en estado Óptimo. ¿Cuál es la probabilidad real de que la siembra germine con éxito dado este pH óptimo?

---

### Solución Paso a Paso

#### Paso 1: Definir los eventos y sus probabilidades a priori
* $G$: La semilla germina con éxito. $\rightarrow P(G) = 0.85$
* $F$: La semilla falla (no germina). $\rightarrow P(F) = 1 - P(G) = 0.15$
* $\text{Óptimo}$: El pH medido es óptimo.
* $P(\text{Óptimo} | G) = 0.90$ (Probabilidad de pH óptimo sabiendo que germina).
* $P(\text{Óptimo} | F) = 0.30$ (Probabilidad de pH óptimo sabiendo que la germinación falla).

#### Paso 2: Plantear el Teorema de Bayes
Queremos calcular la probabilidad a posteriori de germinar dado que medimos pH óptimo, es decir, $P(G | \text{Óptimo})$:

$$P(G | \text{Óptimo}) = \frac{P(\text{Óptimo} | G) \times P(G)}{P(\text{Óptimo} | G) \times P(G) + P(\text{Óptimo} | F) \times P(F)}$$

#### Paso 3: Sustituir los valores y calcular
1. **Numerador (Probabilidad conjunta de germinar y tener pH óptimo):**
   $$P(\text{Óptimo} | G) \times P(G) = 0.90 \times 0.85 = 0.765$$

2. **Denominador (Probabilidad total de obtener un pH óptimo):**
   $$P(\text{Óptimo}) = (0.90 \times 0.85) + (0.30 \times 0.15) = 0.765 + 0.045 = 0.81$$

3. **División final:**
   $$P(G | \text{Óptimo}) = \frac{0.765}{0.81} = 0.9444$$

#### Paso 4: Interpretación
La probabilidad de que las semillas germinen con éxito sube del 85% (a priori) al 94.44% (a posteriori) al comprobar científicamente que el agua del canal posee un pH óptimo.

---

## Ejercicios para Desarrollar en el Cuaderno

Resuelve los siguientes problemas utilizando las fórmulas correspondientes.

### Ejercicio 1: Teorema de Bayes (Estrés Salino en Jitomate)

#### Problema
Un chinampero cultiva jitomate. La probabilidad histórica de que una siembra de jitomate sea de Alta Calidad es del 70% ($P(A) = 0.70$).
El sensor de salinidad mide la conductividad eléctrica. Si la cosecha resulta de Alta Calidad, el nivel de salinidad reportado es Bajo el 80% de las veces ($P(\text{Bajo} | A) = 0.80$). Si la cosecha es de Baja Calidad, la salinidad medida resulta Baja solo el 20% de las veces ($P(\text{Bajo} | B) = 0.20$).

#### Tu Tarea
Si el último reporte de monitoreo indica que la salinidad es Baja:
1. Escribe el Teorema de Bayes adaptado para calcular $P(A | \text{Bajo})$.
2. Realiza las multiplicaciones correspondientes al numerador y al denominador.
3. Determina el porcentaje final de probabilidad de que la cosecha sea de alta calidad.

---

### Ejercicio 2: Distribución Binomial (Riesgo de Desabasto de Cempasúchil)

#### Problema
Para la temporada de Día de Muertos, un productor siembra 8 plantas de cempasúchil en una sección chinampera ($n = 8$). La probabilidad individual de que cada planta florezca a tiempo con el clima actual es de $p = 0.75$ ($75\%$).
La fórmula de la distribución binomial es:
$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$
Donde el coeficiente binomial se calcula como: $\binom{n}{k} = \frac{n!}{k!(n-k)!}$

#### Tu Tarea
El productor tiene un pedido de un cliente que le exige entregar al menos 7 plantas florecidas para no cancelar el contrato.
1. Calcula la probabilidad de que florezcan exactamente 7 plantas ($P(X = 7)$).
2. Calcula la probabilidad de que florezcan exactamente 8 plantas ($P(X = 8)$).
3. Suma ambas probabilidades ($P(X \ge 7) = P(X=7) + P(X=8)$) para obtener la probabilidad de que el productor cumpla con su cliente y no sufra desabasto.
