import os
import webbrowser

from config import OUTPUT_DIR
from etl.extractor import extract_data
from etl.transformer import transform_data
from etl.loader import load_data
from sorting.benchmark import run_benchmarks
from visualization.charts import generate_bar_chart, generate_volume_chart, generate_bar_chart_sin_lentos


def main():
    """
    Orquesta el flujo general del sistema financiero:
    1. Extracción de activos (Yahoo Finance Raw API)
    2. Transformación y Limpieza (Manejo de Nulos vs Calendarios)
    3. Carga y consolidación de Master Dataset
    4. Benchmark de Algoritmos (Calcula Tiempos y Exporta Tablas)
    5. Visualización Estricta
    """
    print("=========================================================")
    print(" INICIO DEL PROYECTO FINANCIERO ALGORÍTMICO")
    print("=========================================================\n")

    extract_data()   # 1. Descarga raw JSON por ticker
    transform_data() # 2. Limpia y exporta CSV individuales
    load_data()      # 3. Consolida en master_dataset.csv

    # 4. Benchmark: mide tiempos y retorna top 15 volumen por activo
    activos_resumen = run_benchmarks()

    # 5. Generar los 3 HTMLs de visualización
    generate_bar_chart()            # Gráfica completa (12 algoritmos, verde)
    generate_bar_chart_sin_lentos() # Gráfica eficientes (9 algoritmos, azul)
    if activos_resumen:
        generate_volume_chart(activos_resumen) # Gráfica top 15 volumen (morado)

    print("=========================================================")
    print(" PROYECTO FINALIZADO EXITOSAMENTE")
    print("=========================================================\n")

    # Abrir los 3 HTMLs en el navegador
    chart_barras    = os.path.join(OUTPUT_DIR, "sorting_chart.html")
    chart_eficientes = os.path.join(OUTPUT_DIR, "sorting_chart_eficientes.html")
    chart_volumen   = os.path.join(OUTPUT_DIR, "volume_chart.html")

    if os.path.exists(chart_barras):
        webbrowser.open(f"file://{os.path.abspath(chart_barras)}")

    if os.path.exists(chart_eficientes):
        webbrowser.open(f"file://{os.path.abspath(chart_eficientes)}")

    if os.path.exists(chart_volumen):
        webbrowser.open(f"file://{os.path.abspath(chart_volumen)}")


if __name__ == "__main__":
    main()