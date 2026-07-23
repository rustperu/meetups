from pathlib import Path

import numpy as np
import pandas as pd


# Cantidad de registros.
# Primero prueba con 1 millón.
# Luego puedes cambiarlo a 5 o 10 millones.
CANTIDAD_REGISTROS = 1_000_000

# Semilla para obtener siempre los mismos datos.
np.random.seed(42)

# Crear la carpeta data si todavía no existe.
carpeta_data = Path("data")
carpeta_data.mkdir(exist_ok=True)

print(f"Creando {CANTIDAD_REGISTROS:,} registros...")

datos = pd.DataFrame(
    {
        "cliente_id": np.random.randint(
            1,
            100_000,
            size=CANTIDAD_REGISTROS,
        ),
        "producto_id": np.random.randint(
            1,
            2_000,
            size=CANTIDAD_REGISTROS,
        ),
        "categoria": np.random.choice(
            [
                "Tecnología",
                "Ropa",
                "Hogar",
                "Deportes",
                "Libros",
                "Alimentos",
            ],
            size=CANTIDAD_REGISTROS,
        ),
        "pais": np.random.choice(
            [
                "Perú",
                "Chile",
                "Colombia",
                "México",
                "Argentina",
            ],
            size=CANTIDAD_REGISTROS,
        ),
        "cantidad": np.random.randint(
            1,
            10,
            size=CANTIDAD_REGISTROS,
        ),
        "precio": np.random.uniform(
            10,
            1000,
            size=CANTIDAD_REGISTROS,
        ).round(2),
    }
)

# Calcular el monto total de cada venta.
datos["monto_total"] = datos["cantidad"] * datos["precio"]

ruta_archivo = carpeta_data / "ventas.parquet"

print("Guardando archivo Parquet...")

datos.to_parquet(
    ruta_archivo,
    index=False,
)

print("Dataset creado correctamente.")
print(f"Ruta: {ruta_archivo}")
print(f"Filas: {len(datos):,}")
print(f"Tamaño: {ruta_archivo.stat().st_size / 1024**2:.2f} MB")

print("\nPrimeras filas:")
print(datos.head())