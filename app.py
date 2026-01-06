from flask import Flask, render_template, request
import csv

app = Flask(__name__)

IVA = 0.19
ARCHIVO_DETALLE = "detalle.csv"
ARCHIVO_MAYOR = "mayor.csv"


def buscar_producto(codigo, archivo):
    with open(archivo, newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f, delimiter=";")

        # Detectar columna de precio automáticamente
        columnas = lector.fieldnames
        columna_precio = None

        for col in columnas:
            if "precio" in col.lower():
                columna_precio = col
                break

        if not columna_precio:
            raise Exception(f"No se encontró columna de precio en {archivo}")

        for fila in lector:
            if fila["codigo"].zfill(6) == codigo:
                precio = int(
                    fila[columna_precio]
                    .replace(".", "")
                    .replace(",", "")
                    .strip()
                )
                return {
                    "codigo": fila["codigo"].zfill(6),
                    "descripcion": fila["descripcion"],
                    "precio": precio
                }
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None

    if request.method == "POST":
        codigo = request.form["codigo"].zfill(6)

        prod_detalle = buscar_producto(codigo, ARCHIVO_DETALLE)
        prod_mayor = buscar_producto(codigo, ARCHIVO_MAYOR)

        if prod_detalle and prod_mayor:
            resultado = {
                "descripcion": prod_detalle["descripcion"],
                "detalle_neto": prod_detalle["precio"],
                "detalle_iva": int(prod_detalle["precio"] * (1 + IVA)),
                "mayor_neto": prod_mayor["precio"],
                "mayor_iva": int(prod_mayor["precio"] * (1 + IVA)),
            }
        else:
            error = "Producto no encontrado"

    return render_template("index.html", resultado=resultado, error=error)


if __name__ == "__main__":
    app.run(debug=True)
