# Python Powered by Rust 🦀

Demo utilizada durante la charla:

## "Cómo Rust está transformando el ecosistema de Ciencia de Datos en Python"

Este repositorio contiene una demostración práctica de cómo herramientas modernas
desarrolladas con Rust pueden integrarse al flujo de trabajo habitual de Python
para Ciencia de Datos.

En particular, la demo compara **Pandas** y **Polars** procesando exactamente el
mismo dataset y realizando las mismas operaciones.

El objetivo no es plantear a Rust como un reemplazo de Python, sino mostrar cómo
ambos lenguajes pueden complementarse: manteniendo la facilidad de uso de Python
mientras se aprovecha el rendimiento de motores desarrollados en Rust.

---

## 🚀 ¿Qué muestra la demo?

Trabajamos con un dataset sintético de:

- 1,000,000 de registros
- Datos de ventas
- Formato Parquet
- Aproximadamente 12.66 MB

Sobre este dataset realizamos exactamente las mismas operaciones:

1. Leer los datos
2. Filtrar ventas con `monto_total > 1000`
3. Agrupar por país y categoría
4. Calcular métricas de ventas
5. Ordenar por ingresos
6. Obtener el Top 10

La comparación se realiza utilizando:

- 🐼 Pandas
- 🐻‍❄️ Polars Eager
- 🐻‍❄️ Polars Lazy

---

## 📁 Estructura del proyecto

    python-powered-by-rust/
    │
    ├── data/
    │   └── ventas.parquet
    │
    ├── src/
    │   ├── 01_crear_dataset.py
    │   ├── 02_pandas.py
    │   ├── 03_polars.py
    │   └── 04_polars_lazy.py
    │
    ├── requirements.txt
    └── README.md

---

## ⚙️ Instalación

Clona el repositorio

Entra al proyecto:

    cd python-powered-by-rust

Crea un entorno virtual:

    python -m venv .venv

Actívalo en macOS/Linux:

    source .venv/bin/activate

En Windows:

    .venv\Scripts\activate

Instala las dependencias:

    pip install -r requirements.txt

---

## 🧪 Ejecutando la demo

### 1. Crear el dataset

    python src/01_crear_dataset.py

Esto genera:

    data/ventas.parquet

con **1,000,000 de registros sintéticos**.

---

### 2. Ejecutar con Pandas 🐼

    python src/02_pandas.py

Ejemplo de resultado obtenido durante la charla:

    Filas leídas: 1,000,000
    Ventas filtradas: 692,416
    Tiempo total Pandas: 2.3608 segundos

---

### 3. Ejecutar con Polars Eager 🐻‍❄️

    python src/03_polars.py

Ejemplo de resultado:

    Filas leídas: 1,000,000
    Ventas filtradas: 692,416
    Tiempo total Polars eager: 0.0500 segundos

En esta ejecución particular:

    Pandas        2.3608 s
    Polars Eager  0.0500 s

Polars utilizó aproximadamente **97.9 % menos tiempo**.

> Los tiempos dependen del hardware, sistema operativo, versiones de las
> librerías y condiciones de ejecución. Estos resultados corresponden a una
> ejecución de la demo y no deben interpretarse como un benchmark universal.

---

## ⚡ Polars Lazy

Polars también permite trabajar utilizando **Lazy Execution**.

En lugar de:

    pl.read_parquet("data/ventas.parquet")

podemos utilizar:

    pl.scan_parquet("data/ventas.parquet")

La diferencia principal es que `scan_parquet()` no ejecuta inmediatamente todas
las operaciones.

Polars construye primero un plan de consulta que puede optimizar antes de
ejecutarlo.

La ejecución ocurre finalmente al utilizar:

    .collect()

Ejecuta el ejemplo:

    python src/04_polars_lazy.py

Durante la demo obtuvimos:

    PROJECT 3/7 COLUMNS
    SELECTION: monto_total > 1000

Esto muestra que Polars pudo determinar que la consulta necesitaba solamente
**3 de las 7 columnas** disponibles y que el filtro podía incorporarse al plan
de lectura.

El resultado obtenido fue:

    Tiempo total Polars lazy: 0.0252 segundos

---

## 📊 Resultados de la demostración

| Herramienta | Tiempo observado |
|---|---:|
| Pandas | 2.3608 s |
| Polars Eager | 0.0500 s |
| Polars Lazy | 0.0252 s |

Todos los ejemplos procesaron el mismo dataset y buscaron producir el mismo
resultado analítico.

⚠️ **Importante:** estos tiempos corresponden a una ejecución concreta de la
demo. Para realizar un benchmark riguroso sería necesario ejecutar múltiples
repeticiones, controlar efectos de caché, versiones, hardware y otras variables.

---

## 💡 Idea principal

La intención de esta demostración no es demostrar que:

> "Python es lento y Rust es rápido."

La idea es mostrar algo mucho más interesante:

**Python y Rust pueden complementarse.**

Python puede seguir proporcionando una API sencilla y familiar para Ciencia de
Datos, mientras herramientas como Polars aprovechan un motor desarrollado en
Rust para realizar el procesamiento.

---

## 👩‍💻 Autora

**Danna Mendez**

Estudiante de Ciencia de Datos.

LinkedIn:  
https://www.linkedin.com/in/danna-mendez-moncada/

---

## 🌷 Sobre la charla

Este repositorio fue preparado como material complementario de la charla.

Si viste la charla y quieres experimentar con el código, puedes clonar el
repositorio, modificar el tamaño del dataset y comparar los resultados en tu
propio equipo.

Los tiempos probablemente serán diferentes. ¡Esa es parte de la idea! 🚀