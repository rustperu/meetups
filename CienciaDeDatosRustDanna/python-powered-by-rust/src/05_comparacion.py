from pathlib import Path
from time import perf_counter

import pandas as pd
import polars as pl


RUTA_DATASET = Path("data/ventas.parquet")


def ejecutar_pandas() -> tuple[float, pd.DataFrame]:
    inicio = perf_counter()

    df = pd.read_parquet(RUTA_DATASET)

    resultado = (
        df[df["monto_total"] > 1000]
        .groupby(
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

    tiempo = perf_counter() - inicio

    return tiempo, resultado


def ejecutar_polars_eager() -> tuple[float, pl.DataFrame]:
    inicio = perf_counter()

    df = pl.read_parquet(RUTA_DATASET)

    resultado = (
        df.filter(
            pl.col("monto_total") > 1000
        )
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

    tiempo = perf_counter() - inicio

    return tiempo, resultado


def ejecutar_polars_lazy() -> tuple[float, pl.DataFrame]:
    inicio = perf_counter()

    resultado = (
        pl.scan_parquet(RUTA_DATASET)
        .select(
            [
                "pais",
                "categoria",
                "monto_total",
            ]
        )
        .filter(
            pl.col("monto_total") > 1000
        )
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
        .collect(
            engine="streaming"
        )
    )

    tiempo = perf_counter() - inicio

    return tiempo, resultado


def main() -> None:
    if not RUTA_DATASET.exists():
        raise FileNotFoundError(
            "Primero ejecuta src/01_crear_dataset.py"
        )

    print("=" * 60)
    print("COMPARACIÓN PANDAS VS POLARS")
    print("=" * 60)

    tiempo_pandas, resultado_pandas = ejecutar_pandas()

    tiempo_polars, resultado_polars = ejecutar_polars_eager()

    tiempo_lazy, resultado_lazy = ejecutar_polars_lazy()

    print("\nRESULTADOS DE TIEMPO")
    print("-" * 60)
    print(f"Pandas:              {tiempo_pandas:.4f} segundos")
    print(f"Polars eager:        {tiempo_polars:.4f} segundos")
    print(f"Polars lazy:         {tiempo_lazy:.4f} segundos")

    if tiempo_polars > 0:
        mejora_eager = tiempo_pandas / tiempo_polars
        print(
            f"\nPolars eager fue aproximadamente "
            f"{mejora_eager:.2f} veces más rápido."
        )

    if tiempo_lazy > 0:
        mejora_lazy = tiempo_pandas / tiempo_lazy
        print(
            f"Polars lazy fue aproximadamente "
            f"{mejora_lazy:.2f} veces más rápido."
        )

    print("\nPrimer resultado con Pandas:")
    print(resultado_pandas.head(1).to_string(index=False))

    print("\nPrimer resultado con Polars:")
    print(resultado_polars.head(1))

    print("\nPrimer resultado con Polars lazy:")
    print(resultado_lazy.head(1))


if __name__ == "__main__":
    main()