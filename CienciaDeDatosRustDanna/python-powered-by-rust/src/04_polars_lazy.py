from time import perf_counter
import polars as pl

RUTA_DATASET = "data/ventas.parquet"

print("=" * 60)
print("ANÁLISIS CON POLARS LAZY")
print("=" * 60)

# Aquí todavía no se cargan todos los datos.
consulta = (
    pl.scan_parquet(RUTA_DATASET)

    # Leer solo las columnas necesarias.
    .select(
        [
            "pais",
            "categoria",
            "monto_total",
        ]
    )

    # Aplicar el filtro.
    .filter(
        pl.col("monto_total") > 1000
    )

    # Agrupar y calcular métricas.
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

    # Ordenar de mayor a menor.
    .sort(
        "ingresos_totales",
        descending=True,
    )
)

print("\nPLAN OPTIMIZADO DE POLARS:")
print(consulta.explain(optimized=True))

print("\nEjecutando consulta...")

inicio = perf_counter()

# Aquí recién se ejecuta todo.
resultado = consulta.collect(
    engine="streaming"
)

tiempo_total = perf_counter() - inicio

print(f"\nTiempo total Polars lazy: {tiempo_total:.4f} segundos")

print("\nTop 10 resultados:")
print(resultado.head(10))

resultado.write_csv(
    "data/resultado_polars_lazy.csv"
)

print("\nResultado guardado en data/resultado_polars_lazy.csv")