from time import perf_counter

import polars as pl


RUTA_DATASET = "data/ventas.parquet"


print("=" * 60)
print("ANÁLISIS CON POLARS EAGER")
print("=" * 60)

inicio_total = perf_counter()

# 1. Leer el archivo completo.
inicio_lectura = perf_counter()

df = pl.read_parquet(RUTA_DATASET)

tiempo_lectura = perf_counter() - inicio_lectura

print(f"\nFilas leídas: {df.height:,}")
print(f"Tiempo de lectura: {tiempo_lectura:.4f} segundos")

# 2. Filtrar, agrupar y ordenar.
inicio_procesamiento = perf_counter()

ventas_filtradas = df.filter(
    pl.col("monto_total") > 1000
)

resultado = (
    ventas_filtradas
    .group_by(
        ["pais", "categoria"]
    )
    .agg(
        pl.len().alias("cantidad_ventas"),
        pl.col("monto_total")
        .sum()
        .alias("ingresos_totales"),
        pl.col("monto_total")
        .mean()
        .alias("venta_promedio"),
    )
    .sort(
        "ingresos_totales",
        descending=True,
    )
)

tiempo_procesamiento = perf_counter() - inicio_procesamiento
tiempo_total = perf_counter() - inicio_total

print(f"Ventas filtradas: {ventas_filtradas.height:,}")
print(
    f"Tiempo de procesamiento: "
    f"{tiempo_procesamiento:.4f} segundos"
)
print(f"Tiempo total Polars eager: {tiempo_total:.4f} segundos")

print("\nTop 10 resultados:")
print(resultado.head(10))

resultado.write_csv(
    "data/resultado_polars.csv"
)

print("\nResultado guardado en data/resultado_polars.csv")