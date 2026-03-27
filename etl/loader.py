import os
import csv
from config import CLEAN_DIR, MASTER_DIR


def load_data():

    # Consolida todos los CSV individuales de la carpeta clean en un único "master_dataset.csv".
    # Complejidad Temporal: O(C * F), donde C = número total de filas en todos los archivos F.
    # Complejidad Espacial: O(1) de forma asintótica por utilizar escritura iterativa mediante streams (sin engullir todos los datos).

    print("Iniciando Loader ETL (Módulo de Carga)...")
    archivos = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]

    master_file_path = os.path.join(MASTER_DIR, "master_dataset.csv")
    fieldnames = ['fecha', 'ticker', 'open', 'high', 'low', 'close', 'volumen']

    total_filas = 0
    with open(master_file_path, "w", newline="", encoding="utf-8") as master_f:
        writer = csv.DictWriter(master_f, fieldnames=fieldnames)
        writer.writeheader()

        for archivo in archivos:
            with open(os.path.join(CLEAN_DIR, archivo), "r", encoding="utf-8") as in_file:
                reader = csv.DictReader(in_file)
                for row in reader:
                    # Garantizar el orden de las columnas requeridas
                    sorted_row = {
                        'fecha': row['fecha'],
                        'ticker': row['ticker'],
                        'open': row['open'],
                        'high': row['high'],
                        'low': row['low'],
                        'close': row['close'],
                        'volumen': row['volumen']
                    }
                    writer.writerow(sorted_row)
                    total_filas += 1

    print(f" -> Carga finalizada existosamente en {master_file_path}")
    print(f" -> Total registros en Master Dataset: {total_filas}\n")
    return master_file_path


if __name__ == "__main__":
    load_data()
