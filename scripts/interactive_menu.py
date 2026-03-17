"""
SCRIPT 3: Interactive Menu (Visualización y búsqueda de datos)
===============================================================
Menú interactivo para visualizar datos, generar gráficos y buscar
institutos por ciclo formativo o enseñanza.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sns.set_theme(style="whitegrid")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CLEAN_FILE = os.path.join(DATA_DIR, 'institutos_limpios.csv')


def cargar_datos():
    """Carga datos limpios o regenera si es necesario"""
    print("=" * 70)
    print("SCRIPT 3: MENÚ INTERACTIVO - Visualización y búsqueda")
    print("=" * 70)

    if not os.path.exists(CLEAN_FILE):
        print(f"\n[!] Error: No se encuentra '{CLEAN_FILE}'")
        print(f"    Ejecuta primero: python scripts/data_cleaner.py")
        return None

    print(f"\n[*] Cargando datos desde: {CLEAN_FILE}")
    df = pd.read_csv(CLEAN_FILE)
    print(f"    Total de institutos cargados: {len(df)}")
    return df


def mostrar_graficos(df):
    """Genera y muestra gráficos de distribución"""
    print("\n[*] Generando gráficos... Cierra la ventana para volver al menú.\n")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico 1: Titularidad
    sns.countplot(
        data=df, x='titularidad', hue='titularidad',
        palette='viridis', legend=False, ax=axes[0]
    )
    axes[0].set_title('Distribución de IES y FP por Titularidad', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Titularidad', fontsize=12)
    axes[0].set_ylabel('Cantidad de Centros', fontsize=12)

    # Gráfico 2: Top 10 municipios
    top_municipios = df['municipio'].value_counts().head(10)
    sns.barplot(
        y=top_municipios.index, x=top_municipios.values,
        hue=top_municipios.index, palette='magma', legend=False, ax=axes[1]
    )
    axes[1].set_title('Top 10 Municipios con más IES y Centros de FP', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Número de Institutos', fontsize=12)
    axes[1].set_ylabel('Municipio', fontsize=12)

    plt.tight_layout()
    plt.show()


def buscar_por_ciclo(df):
    """Permite buscar institutos por ciclo/enseñanza"""
    ciclo = input(
        "\nIntroduce el nombre o palabra clave "
        "(ej. 'Informática', 'Sanidad', 'Administración', 'Deporte'): "
    ).strip()

    if not ciclo:
        print("[!] Búsqueda vacía. Volviendo al menú...")
        return

    cols = ['especialidad', 'familia_fp']
    mascara = pd.Series(False, index=df.index)

    for col in cols:
        if col in df.columns:
            mascara |= df[col].fillna('').str.contains(ciclo, case=False, regex=False)

    resultados = df[mascara]

    if resultados.empty:
        print(f"\n[!] No se encontraron centros con '{ciclo}'.")
        print("\n    Sugerencias de búsqueda:")
        print("    - Informática, Sanidad, Administración")
        print("    - Hostelería, Deporte, Social")
        print("    - Marketing, Imagen Personal, Electricidad")
    else:
        cols_mostrar = ['nombre', 'tipo', 'municipio', 'titularidad', 'familia_fp']
        print(f"\n{'=' * 70}")
        print(f"    {len(resultados)} centros encontrados para '{ciclo}'")
        print(f"{'=' * 70}\n")
        print(resultados[cols_mostrar].head(20).to_string(index=False))
        if len(resultados) > 20:
            print(f"\n    ... y {len(resultados) - 20} resultados más.")
        print()


def buscar_por_municipio(df):
    """Permite buscar institutos por municipio"""
    municipios = sorted(df['municipio'].unique())

    print(f"\n{'=' * 70}")
    print("    TOP 20 MUNICIPIOS")
    print(f"{'=' * 70}")
    top_20 = df['municipio'].value_counts().head(20)
    for i, (mun, count) in enumerate(top_20.items(), 1):
        print(f"    {i:2}. {mun:40} ({count} institutos)")
    print()

    municipio = input("    Introduce nombre del municipio (o Enter para cancelar): ").strip()

    if not municipio:
        print("    [!] Búsqueda cancelada. Volviendo al menú...")
        return

    resultados = df[df['municipio'].str.contains(municipio, case=False, regex=False)]

    if resultados.empty:
        print(f"\n    [!] No se encontraron centros en '{municipio}'.")
    else:
        cols_mostrar = ['nombre', 'tipo', 'titularidad', 'familia_fp']
        print(f"\n{'=' * 70}")
        print(f"    {len(resultados)} centros en {municipio}")
        print(f"{'=' * 70}\n")
        print(resultados[cols_mostrar].to_string(index=False))
        print()


def menu_principal():
    """Menú principal interactivo"""
    df = cargar_datos()

    if df is None:
        return

    while True:
        print("\n" + "=" * 70)
        print("   MENÚ DE GESTIÓN DE INSTITUTOS FP/IES - COMUNIDAD DE MADRID")
        print("=" * 70)
        print("  1. Mostrar gráficos de distribución")
        print("  2. Buscar institutos por ciclo/enseñanza")
        print("  3. Buscar institutos por municipio")
        print("  4. Ver información general")
        print("  5. Salir")
        print("=" * 70)

        opcion = input("  Elige una opción (1-5): ").strip()

        if opcion == '1':
            mostrar_graficos(df)
        elif opcion == '2':
            buscar_por_ciclo(df)
        elif opcion == '3':
            buscar_por_municipio(df)
        elif opcion == '4':
            print(f"\n{'=' * 70}")
            print("    INFORMACIÓN GENERAL")
            print(f"{'=' * 70}")
            print(f"    Total de institutos: {len(df)}")
            print(f"    Municipios: {df['municipio'].nunique()}")
            print(f"    Tipos de centro: {df['tipo'].nunique()}")
            print(f"    Titularidad: {df['titularidad'].nunique()}")
            print(f"    Familias FP: {df['familia_fp'].nunique()}")
            print()
        elif opcion == '5':
            print("\n[*] ¡Hasta pronto!\n")
            sys.exit(0)
        else:
            print("\n[!] Opción no válida. Elige 1, 2, 3, 4 o 5.")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n[*] Programa interrumpido por el usuario.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}\n")
        sys.exit(1)

