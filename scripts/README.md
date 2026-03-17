"""
SCRIPTS - Procesamiento y visualización de datos
==================================================

Este directorio contiene scripts Python para procesar y visualizar datos
de institutos educativos de la Comunidad de Madrid.

IMPORTANTE: Estos scripts son INDEPENDIENTES de Django y pueden ejecutarse
desde línea de comandos. Django se ejecuta desde el directorio raíz.

---

SCRIPT 1: data_cleaner.py
-----------
PROPÓSITO:
  Limpia y enriquece datos brutos de institutos educativos.
  Lee centros_merged.csv y genera institutos_limpios.csv con:
  - Filtrado por tipo (IES, CIFP, CPR FP, etc.)
  - Eliminación de registros sin coordenadas GPS
  - Clasificación automática por familia FP (Informática, Sanidad, etc.)

USO:
  python scripts/data_cleaner.py

ENTRADA:
  data/centros_merged.csv

SALIDA:
  data/institutos_limpios.csv

---

SCRIPT 2: web_scraper.py
----------
PROPÓSITO:
  Scrappea el portal del Ministerio de Educación para extraer ciclos
  formativos específicos de cada instituto.
  
ADVERTENCIA:
  - Requiere conexión a Internet
  - Introduce delays entre peticiones (0.8s) para no sobrecargar servidor
  - Puede tardar MUCHO tiempo (horas) en completarse

USO:
  python scripts/web_scraper.py

ENTRADA:
  data/institutos_sin_ciclos_especificos.csv

SALIDA:
  data/ciclos_scrapeados.csv

---

SCRIPT 3: interactive_menu.py
-----------
PROPÓSITO:
  Menú interactivo para visualizar y buscar datos de institutos.
  Permite:
  - Ver gráficos de distribución por titularidad y municipio
  - Buscar institutos por ciclo formativo
  - Buscar institutos por municipio
  - Ver información general

USO:
  python scripts/interactive_menu.py

REQUISITOS:
  data/institutos_limpios.csv (generado por data_cleaner.py)

---

FLUJO DE TRABAJO RECOMENDADO
=============================

1. LIMPIEZA DE DATOS:
   python scripts/data_cleaner.py
   
   → Genera: data/institutos_limpios.csv

2. (OPCIONAL) SCRAPING WEB:
   python scripts/web_scraper.py
   
   → Genera: data/ciclos_scrapeados.csv
   → Nota: Solo si necesitas ciclos específicos muy detallados

3. EXPLORACIÓN DE DATOS:
   python scripts/interactive_menu.py
   
   → Visualiza datos y permite búsquedas interactivas

4. CARGAR EN DJANGO:
   python manage.py load_data
   
   → Importa institutos en la BD de Django
   → Permite acceso vía API REST

---

ESTRUCTURA DE DATOS
====================

centros_merged.csv (INPUT - archivo original)
├─ Campos: código, nombre, tipo, titularidad, municipio, direccion, etc.
└─ Contiene TODOS los centros educativos (no filtrado)

↓ (data_cleaner.py procesa)

institutos_limpios.csv (INTERMEDIO - después de limpieza)
├─ Solo centros de tipo IES/FP
├─ Con coordenadas GPS válidas
├─ Enriquecido con familia_fp y especialidad
└─ Listo para visualización y carga en BD

↓ (load_data.py procesa)

BD Django (FINAL - base de datos del API)
├─ Modelos: Instituto, CicloFormativo
├─ Acceso vía: GET /api/institutos/
└─ Búsqueda vía: GET /api/institutos/?municipio=Madrid

---

REQUISITOS (si ejecutas scripts standalone)
=============================================

pip install pandas
pip install requests
pip install beautifulsoup4
pip install matplotlib
pip install seaborn
pip install tqdm

O instalar todos los requirements del proyecto:
pip install -r requirements.txt

---

NOTAS IMPORTANTES
=================

1. Los scripts usan rutas relativas. Ejecutarlos desde la raíz del proyecto:
   
   ✓ CORRECTO:  cd C:\...\Trabajo-API-REST && python scripts/data_cleaner.py
   ✗ INCORRECTO: cd C:\...\Trabajo-API-REST\scripts && python data_cleaner.py

2. data_cleaner.py es RÁPIDO (~segundos)
3. web_scraper.py es MUY LENTO (~horas por cientos de institutos)
4. interactive_menu.py requiere data/institutos_limpios.csv

---

TROUBLESHOOTING
===============

"FileNotFoundError: data/centros_merged.csv"
→ Asegúrate de que el archivo existe en data/

"ModuleNotFoundError: No module named 'pandas'"
→ pip install pandas

"No se conecta al servidor del ministerio"
→ Comprueba tu conexión a Internet y permisos de red

"Script está tardando mucho"
→ Es normal si ejecutas web_scraper.py (puede tardar horas)
→ Puedes interrumpir con Ctrl+C (perderás progreso actual)


