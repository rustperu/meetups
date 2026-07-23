from time import perf_counter

import pandas as pd


RUTA_DATASET = "data/ventas.parquet"


print("=" * 60)
print("ANÁLISIS CON PANDAS")
print("=" * 60)

inicio_total = perf_counter()

# 1. Leer el archivo.
inicio_lectura = perf_counter()

df = pd.read_parquet(RUTA_DATASET)

tiempo_lectura = perf_counter() - inicio_lectura

print(f"\nFilas leídas: {len(df):,}")
print(f"Tiempo de lectura: {tiempo_lectura:.4f} segundos")

# 2. Filtrar ventas mayores a 1000.
inicio_procesamiento = perf_counter()

ventas_filtradas = df[df["monto_total"] > 1000].copy()

# 3. Agrupar por país y categoría.
resultado = (
    ventas_filtradas.groupby(
        ["pais", "categoria"],
        as_index=False,
    )
    .agg(
        cantidad_ventas=("monto_total", "count"),
        ingresos_totales=("monto_total", "sum"),
        venta_promedio=("monto_total", "mean"),
    )
    .sort_values(
        "ingresos_totales",
        ascending=False,
    )
)

tiempo_procesamiento = perf_counter() - inicio_procesamiento
tiempo_total = perf_counter() - inicio_total

print(f"Ventas filtradas: {len(ventas_filtradas):,}")
print(
    f"Tiempo de procesamiento: "
    f"{tiempo_procesamiento:.4f} segundos"
)
print(f"Tiempo total Pandas: {tiempo_total:.4f} segundos")

print("\nTop 10 resultados:")
print(resultado.head(10).to_string(index=False))

resultado.to_csv(
    "data/resultado_pandas.csv",
    index=False,
)

print("\nResultado guardado en data/resultado_pandas.csv")