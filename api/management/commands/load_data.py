"""
=============================================================================
 ALUMNO 1 — PASO 3: LOAD (Ingesta de datos)
 Management Command de Django
=============================================================================
 Uso:
     python manage.py load_data
     python manage.py load_data --csv ruta/al/archivo.csv
     python manage.py load_data --reset       # borra la BD antes de cargar

 Qué hace:
     1. Lee 'institutos_limpios.csv' (generado por main.py - pasos 1 y 2)
     2. Por cada fila, crea o actualiza un Instituto en la BBDD (get_or_create)
     3. Parsea las especialidades de cada instituto y crea los CicloFormativo
     4. Vincula cada Instituto con sus Ciclos vía la relación ManyToMany
     5. Muestra un resumen final con totales

 Modelos que usa (definidos por Alumno 2 en api/models.py):
     - Instituto  (nombre, direccion, distrito, latitud, longitud, ciclos M2M)
     - CicloFormativo  (nombre, familia_profesional, grado)
=============================================================================
"""

import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from api.models import Instituto, CicloFormativo


# ─────────────────────────────────────────────────────────────────────────────
# Mapeado de grado a partir del nombre del ciclo
# ─────────────────────────────────────────────────────────────────────────────
def _inferir_grado(nombre_ciclo: str) -> str:
    """
    Deduce el grado formativo a partir del nombre del ciclo.
    Devuelve: 'GM' (Grado Medio), 'GS' (Grado Superior) o 'FPB' (FP Básica).
    """
    nombre_up = nombre_ciclo.upper()
    if 'BÁSICA' in nombre_up or 'BASICA' in nombre_up or 'FP BÁSICA' in nombre_up:
        return 'FPB'
    if 'SUPERIOR' in nombre_up or 'CFGS' in nombre_up:
        return 'GS'
    if 'MEDIO' in nombre_up or 'CFGM' in nombre_up or 'TÉCNICO EN' in nombre_up:
        return 'GM'
    # Fallback: si el nombre empieza por "Técnico Superior" → GS
    if nombre_ciclo.startswith('Técnico Superior'):
        return 'GS'
    if nombre_ciclo.startswith('Técnico en') or nombre_ciclo.startswith('Técnico '):
        return 'GM'
    return 'GS'  # valor por defecto conservador


def _parsear_ciclos(especialidad_str: str, familia: str) -> list[dict]:
    """
    Convierte la columna 'especialidad' (nombres separados por ' | ')
    en una lista de dicts {nombre, familia_profesional, grado}.

    Ejemplo de entrada:
        'Técnico en Gestión Administrativa | Técnico Superior en Administración y Finanzas'
    Ejemplo de salida:
        [
            {'nombre': 'Técnico en Gestión Administrativa',
             'familia_profesional': 'Administración y Gestión', 'grado': 'GM'},
            {'nombre': 'Técnico Superior en Administración y Finanzas',
             'familia_profesional': 'Administración y Gestión', 'grado': 'GS'},
        ]
    """
    ciclos = []
    if not especialidad_str or pd.isna(especialidad_str):
        return ciclos

    # Ignorar valores genéricos que no corresponden a ciclos reales
    IGNORAR = {
        'ESO | Bachillerato | Ciclos Formativos',
        'ESO | Bachillerato | Ciclos Formativos GM y GS',
        'Ciclos Formativos de Grado Medio y Superior',
        'ESO | Bachillerato | Ciclos Formativos de GM y GS',
    }
    if especialidad_str.strip() in IGNORAR:
        return ciclos

    for parte in especialidad_str.split('|'):
        nombre_ciclo = parte.strip()
        if not nombre_ciclo or len(nombre_ciclo) < 5:
            continue
        ciclos.append({
            'nombre':             nombre_ciclo,
            'familia_profesional': str(familia).strip() if pd.notna(familia) else 'Sin clasificar',
            'grado':              _inferir_grado(nombre_ciclo),
        })
    return ciclos


# ─────────────────────────────────────────────────────────────────────────────
# Management Command
# ─────────────────────────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = 'PASO 3 LOAD — Carga institutos y ciclos formativos desde el CSV limpio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default=os.path.join('data', 'institutos_limpios.csv'),
            help='Ruta al CSV limpio (default: data/institutos_limpios.csv)',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los institutos y ciclos antes de cargar (útil en desarrollo)',
        )

    # ── Punto de entrada ──────────────────────────────────────────────────────
    def handle(self, *args, **options):
        csv_path = options['csv']

        # ── Verificar archivo ─────────────────────────────────────────────────
        if not os.path.exists(csv_path):
            raise CommandError(
                f"\n[!] No se encontró el archivo: '{csv_path}'\n"
                f"    Asegúrate de haber ejecutado main.py (pasos 1 y 2) primero."
            )

        # ── Reset opcional ────────────────────────────────────────────────────
        if options['reset']:
            self.stdout.write(self.style.WARNING("⚠  --reset activado: borrando datos existentes..."))
            Instituto.objects.all().delete()
            CicloFormativo.objects.all().delete()
            self.stdout.write("   Tablas vaciadas.\n")

        # ── Leer CSV ──────────────────────────────────────────────────────────
        self.stdout.write(f"📂 Leyendo archivo: {csv_path}")
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except Exception as e:
            raise CommandError(f"Error al leer el CSV: {e}")

        self.stdout.write(f"   Filas encontradas: {len(df)}\n")

        # ── Contadores ────────────────────────────────────────────────────────
        inst_creados    = 0
        inst_actualizados = 0
        ciclos_creados  = 0
        errores         = 0

        # ── Iterar filas ──────────────────────────────────────────────────────
        for index, row in df.iterrows():
            try:
                # ── 1. Crear o actualizar Instituto ───────────────────────────
                # get_or_create busca por 'nombre'; si no existe, lo crea con defaults
                instituto, creado = Instituto.objects.get_or_create(
                    codigo=int(row['codigo']) if pd.notna(row.get('codigo')) else 0,
                    defaults={
                        'nombre':       str(row['nombre']).strip(),
                        'tipo':         str(row.get('tipo', '')).strip()
                                        if pd.notna(row.get('tipo')) else '',
                        'titularidad':  str(row.get('titularidad', '')).strip()
                                        if pd.notna(row.get('titularidad')) else '',
                        'municipio':    str(row.get('municipio', '')).strip()
                                        if pd.notna(row.get('municipio')) else '',
                        'direccion':    str(row.get('direccion', '')).strip()
                                        if pd.notna(row.get('direccion')) else '',
                        'codigo_postal': str(int(row['codigo_postal'])) if pd.notna(row.get('codigo_postal')) else '',
                        'telefono':     str(row.get('telefono', '')).strip()
                                        if pd.notna(row.get('telefono')) else '',
                        'email':        str(row.get('email', '')).strip()
                                        if pd.notna(row.get('email')) else '',
                        'web':          str(row.get('web', '')).strip()
                                        if pd.notna(row.get('web')) else '',
                        'latitud':      float(row['latitud'])  if pd.notna(row.get('latitud'))  else 0.0,
                        'longitud':     float(row['longitud']) if pd.notna(row.get('longitud')) else 0.0,
                        'situacion':    str(row.get('situacion', '')).strip()
                                        if pd.notna(row.get('situacion')) else '',
                    }
                )

                # Si ya existía, actualizamos sus coordenadas por si han cambiado
                if not creado:
                    updated = False
                    if pd.notna(row.get('latitud')) and instituto.latitud != float(row['latitud']):
                        instituto.latitud = float(row['latitud'])
                        updated = True
                    if pd.notna(row.get('longitud')) and instituto.longitud != float(row['longitud']):
                        instituto.longitud = float(row['longitud'])
                        updated = True
                    if updated:
                        instituto.save()
                    inst_actualizados += 1
                else:
                    inst_creados += 1

                # ── 2. Parsear ciclos de la fila ──────────────────────────────
                ciclos_data = _parsear_ciclos(
                    row.get('especialidad', ''),
                    row.get('familia_fp', 'Sin clasificar')
                )

                # ── 3. Crear ciclos y vincular con el instituto ────────────────
                for ciclo_data in ciclos_data:
                    ciclo, ciclo_creado = CicloFormativo.objects.get_or_create(
                        nombre=ciclo_data['nombre'],
                        defaults={
                            'familia_profesional': ciclo_data['familia_profesional'],
                            'grado':               ciclo_data['grado'],
                        }
                    )
                    if ciclo_creado:
                        ciclos_creados += 1

                    # Vincular si no está ya vinculado (M2M evita duplicados con add)
                    instituto.ciclos.add(ciclo)

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f"   [!] Error en fila {index} "
                                     f"({row.get('nombre', '?')}): {e}")
                )

        # ── Resumen final ─────────────────────────────────────────────────────
        self.stdout.write("\n" + "─" * 50)
        self.stdout.write(self.style.SUCCESS("✅ Carga completada"))
        self.stdout.write("─" * 50)
        self.stdout.write(f"  Institutos creados:      {inst_creados}")
        self.stdout.write(f"  Institutos actualizados: {inst_actualizados}")
        self.stdout.write(f"  Ciclos creados:          {ciclos_creados}")
        self.stdout.write(f"  Total institutos en BD:  {Instituto.objects.count()}")
        self.stdout.write(f"  Total ciclos en BD:      {CicloFormativo.objects.count()}")
        if errores:
            self.stdout.write(self.style.WARNING(f"  Filas con error:         {errores}"))
        self.stdout.write("─" * 50 + "\n")
        self.stdout.write("  Puedes verificar los datos en:")
        self.stdout.write("  → http://127.0.0.1:8000/admin/")
        self.stdout.write("  → http://127.0.0.1:8000/api/institutos/\n")
