import os
import json
import csv
import datetime
from config import RAW_DIR, CLEAN_DIR

def transform_data():
    print("Iniciando Transformador ETL...")
    archivos = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]

    for archivo in archivos:
        with open(os.path.join(RAW_DIR, archivo), "r", encoding="utf-8") as f:
            data = json.load(f)

        ticker = archivo.replace(".json", "")

        try:
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]

            opens = quote.get('open', [])
            closes = quote.get('close', [])
            highs = quote.get('high', [])
            lows = quote.get('low', [])
            volumes = quote.get('volume', [])
        except (KeyError, IndexError, TypeError):
            print(f" -> JSON con estructura anómala, saltando: {ticker}")
            continue

        registros_limpios = []

        # Variables para arrastre de nulos
        last_open, last_close, last_high, last_low = 0.0, 0.0, 0.0, 0.0

        nulos_encontrados = {
            'open': 0, 'close': 0, 'high': 0, 'low': 0, 'volumen': 0
        }

        for i in range(len(timestamps)):
            t = timestamps[i]
            o = opens[i] if i < len(opens) else None
            c = closes[i] if i < len(closes) else None
            h = highs[i] if i < len(highs) else None
            l = lows[i] if i < len(lows) else None
            v = volumes[i] if i < len(volumes) else None

            # Manejo de NULOS
            # Justificación: Al ser datos de mercado continuo, un nulo suele representar días inactivos,
            # caídas de la API, o congelamiento. Usaremos 'carry-forward' (repetir último previo válido)
            # para no romper continuidades de indicadores, lo cual es la práctica estándar en finanzas.

            if o is None:
                o = last_open
            else:
                last_open = o

            if c is None:
                c = last_close
            else:
                last_close = c

            if h is None:
                h = last_high
            else:
                last_high = h

            if l is None:
                l = last_low
            else:
                last_low = l

            if v is None: v = 0  # El volumen puede ser 0 razonablemente si estuvo inactivo

            # Normalización de timestamp a fecha YYYY-MM-DD
            dt = datetime.datetime.fromtimestamp(t)
            fecha_str = dt.strftime('%Y-%m-%d')

            # Si a pesar del carry-forward sigue en 0 dictamos un skip (primeros datos de la historia nulos)
            if c == 0.0:
                continue

            registros_limpios.append({
                'fecha': fecha_str,
                'open': round(o, 4),
                'high': round(h, 4),
                'low': round(l, 4),
                'close': round(c, 4),
                'volumen': int(v),
                'ticker': ticker
            })

        # Exportar a Clean CSV
        csv_path = os.path.join(CLEAN_DIR, f"{ticker}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=['fecha', 'open', 'high', 'low', 'close', 'volumen', 'ticker'])
            writer.writeheader()
            writer.writerows(registros_limpios)

        print(f" -> Transformado: {ticker}.csv ({len(registros_limpios)} filas)")

        print(f" -> Nulos detectados en {ticker}: {nulos_encontrados}\n")

    print("Transformación completada.\n")


if __name__ == "__main__":
    transform_data()