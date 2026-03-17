"""
SCRIPT 2: Web Scraper (Obtener ciclos formativos del portal educativo)
========================================================================
Lee institutos_sin_ciclos_especificos.csv y scrappea la web del ministerio
para extraer ciclos formativos, guardando resultado en ciclos_scrapeados.csv
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import re
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

INPUT_FILE = os.path.join(DATA_DIR, 'institutos_sin_ciclos_especificos.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'ciclos_scrapeados.csv')

BASE_URL = "https://www.educacion.gob.es/centros/centro.do?codigo="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

FP_KEYWORDS = [
    "grado medio",
    "grado superior",
    "fp básica",
    "formación profesional",
    "ciclo formativo"
]


def is_fp_text(text):
    """Comprueba si el texto contiene referencias a FP"""
    t = text.lower()
    return any(k in t for k in FP_KEYWORDS)


def clean_cycle(text):
    """Limpia espacios en blanco del nombre de ciclo"""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def scrape_centro(codigo):
    """Scrappea un centro individual del portal educativo"""
    url = BASE_URL + str(codigo)

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        if r.status_code != 200:
            return {
                "codigo": codigo,
                "ciclos": "",
                "familias_fp": "",
                "status": "http_error"
            }

        soup = BeautifulSoup(r.text, "lxml")

        ciclos = set()
        familias = set()

        # TABLE PARSING
        for table in soup.find_all("table"):
            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all(["td", "th"])
                texts = [c.get_text(" ", strip=True) for c in cells]
                row_text = " ".join(texts)

                if is_fp_text(row_text):
                    for t in texts:
                        t = clean_cycle(t)
                        if len(t) < 4:
                            continue
                        if is_fp_text(t):
                            continue

                        ciclos.add(t)

                        # detect possible FP family
                        if re.search(
                            r"informat|sanidad|admin|electric|hosteler|imagen|transporte|quimic|agrar",
                            t.lower()
                        ):
                            familias.add(t)

        # LIST PARSING (<li>)
        for li in soup.find_all("li"):
            text = clean_cycle(li.get_text(" ", strip=True))

            if is_fp_text(text):
                parts = re.split(r":|-", text)

                if len(parts) > 1:
                    ciclos.add(clean_cycle(parts[-1]))
                else:
                    ciclos.add(text)

        # TEXT BLOCK PARSING
        for p in soup.find_all(["p", "div"]):
            text = clean_cycle(p.get_text(" ", strip=True))

            if is_fp_text(text) and len(text) < 150:
                parts = re.split(r":|-", text)

                if len(parts) > 1:
                    ciclos.add(clean_cycle(parts[-1]))

        ciclos_clean = sorted([c for c in ciclos if len(c) > 4])
        familias_clean = sorted(familias)

        status = "ok" if ciclos_clean else "no_fp_found"

        return {
            "codigo": codigo,
            "ciclos": "; ".join(ciclos_clean),
            "familias_fp": "; ".join(familias_clean),
            "status": status
        }

    except Exception as e:
        return {
            "codigo": codigo,
            "ciclos": "",
            "familias_fp": "",
            "status": "error"
        }


def main():
    print("=" * 70)
    print("SCRIPT 2: WEB SCRAPER - Extracción de ciclos formativos")
    print("=" * 70)

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(INPUT_FILE):
        print(f"\n[!] Error: No se encuentra '{INPUT_FILE}'")
        print(f"    Necesario ejecutar primero: scripts/data_cleaner.py")
        return False

    print(f"\n[*] Cargando institutos desde: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    codigos = df["codigo"].unique()
    print(f"    Total de códigos a scrappear: {len(codigos)}")

    print(f"\n[*] Iniciando scraping (delay 0.8s entre peticiones)...")
    resultados = []

    for codigo in tqdm(codigos, desc="Scraping"):
        data = scrape_centro(codigo)
        resultados.append(data)
        time.sleep(0.8)

    result_df = pd.DataFrame(resultados)

    print(f"\n[*] Guardando resultados en: {OUTPUT_FILE}")
    result_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n[*] Resumen de scraping:")
    print(result_df["status"].value_counts())

    print("\n[✓] Web Scraper completado exitosamente")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

