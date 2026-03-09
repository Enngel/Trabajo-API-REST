import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sns.set_theme(style="whitegrid")

RUTA_ORIGEN = os.path.join('proyecto_institutos', 'data', 'centros_merged.csv')
RUTA_LIMPIO = os.path.join('proyecto_institutos', 'data', 'institutos_limpios.csv')


# ─────────────────────────────────────────────────────────────────────────────
# MAPEADO KEYWORDS → familia FP oficial (catálogo LOMLOE)
# ─────────────────────────────────────────────────────────────────────────────
KEYWORD_MAP = [
    (['INFORMATICA','INFORMÁTICA','NUEVAS TECNOLOG','TECNOLOG','DIGITAL','CYBER','CIBER',
      'SOFTWARE','PROGRAMACION','PROGRAMACIÓN','DATOS','DATA','INTERNET','REDES','NETWORK',
      'UNIVERSOFT','MICROFORUM','CIBERNOS','VODAFONE','UDIMA','DIGITECH','CDM INFINIA',
      'WINTRAIN','CORE NETWORKS','CAMPUS FP VISTALEGRE','CAMPUS FP ALCALA DE HENARES IT'],
     'Informática y Comunicaciones',
     'Administración de Sistemas Informáticos en Red | Desarrollo de Aplicaciones Web | '
     'Desarrollo de Aplicaciones Multiplataforma | Ciberseguridad en Entornos TI',
     'CFGM|CFGS'),

    (['SALUD','SANIDAD','SANITAR','MEDIC','BIOSANITARI','HOSPITAL','DENTAL','ENFERMERIA',
      'ENFERMERÍA','FARMACIA','LABORATORI','CLINICO','CLÍNICO','HUMANIZACION','GALENO',
      'XTART','MEDAC','SANITAS','BOBATH','CAMPUS DENTAL','GRUPO CTO','FORMA-T',
      'INGENIERIA CLINICA','CAMPUS FP SOCIOSANITARIO'],
     'Sanidad',
     'Técnico en Cuidados Auxiliares de Enfermería | Técnico Superior en Laboratorio Clínico '
     'y Biomédico | Técnico Superior en Imagen para el Diagnóstico | Técnico Superior en Salud Ambiental',
     'CFGM|CFGS'),

    (['ADMINISTRACION','ADMINISTRACIÓN','GESTION','GESTIÓN','EMPRESARIAL','FINANCIER',
      'FINANZAS','NEGOCIOS','CAMARA DE COMERCIO','CENTRO DE ESTUDIOS FINANCIEROS','ALTA DIRECCION',
      'ESERP','ESIC','AEI BUSINESS','BUSINESS AND LANGUAGE','FORMACION COMERCIAL','IMF',
      'ADAMS FP','FP SUMMA','CEF','ABACO','CARDENAL CISNEROS','JOVELLANOS','FOMENTO'],
     'Administración y Gestión',
     'Técnico en Gestión Administrativa | Técnico Superior en Administración y Finanzas | '
     'Técnico Superior en Asistencia a la Dirección',
     'CFGM|CFGS'),

    (['HOSTELERIA','HOSTELERÍA','TURISMO','GASTRONOMIA','GASTRONOMÍA','COCINA','CULINARI',
      'RESTAURACION','RESTAURACIÓN','C.D.TUR','SIMONE ORTEGA','ESCUELA DE LA VID',
      'ESC. HOSTELERIA','MOM CULINARY','ESATUR','CENTRO SUPERIOR DE HOSTELERIA'],
     'Hostelería y Turismo',
     'Técnico en Cocina y Gastronomía | Técnico Superior en Dirección de Cocina | '
     'Técnico Superior en Gestión de Alojamientos Turísticos | '
     'Técnico Superior en Agencias de Viajes y Gestión de Eventos',
     'CFGM|CFGS'),

    (['IMAGEN Y SONIDO','AUDIOVISUAL','CINE','VIDEO','SONIDO','RADIO','TELEVISION',
      'RTVE','FOTOGRAFIA','FOTOGRAFÍA','PUBLICIDAD','PRENSA','CEV','CES IMAGEN',
      'VOXEL','TRAZOS','INFOGRAFIA','UDIT','IED MADRID','COMUNICACION AUDIOVISUAL',
      'CAMPUS FP ARGANDA'],
     'Comunicación, Imagen y Sonido',
     'Técnico Superior en Producción de Audiovisuales | '
     'Técnico Superior en Realización de Proyectos Audiovisuales | '
     'Técnico Superior en Imagen | Técnico Superior en Sonido para Audiovisuales',
     'CFGS'),

    (['PELUQUERIA','PELUQUERÍA','ESTETICA','ESTÉTICA','BELLEZA','NOVELLA','IMAGEN PERSONAL'],
     'Imagen Personal',
     'Técnico en Peluquería y Cosmética Capilar | '
     'Técnico Superior en Estética Integral y Bienestar | '
     'Técnico Superior en Asesoría de Imagen Personal y Corporativa',
     'CFGM|CFGS'),

    (['SOCIAL','SOCIOSANIT','ATENCION PERSON','DEPENDENCIA','EDUCACION INFANTIL',
      'EDUCACIÓN INFANTIL','TOMILLO','FUNDACION TOMILLO','CRUZ ROJA','JUAN LUIS MARROQUIN',
      'RECURSOS COM.SORDA','CAMPUS FP FUNDACION APROCOR','JUAN XXIII','MURIALDO',
      'SAN JOSE OBRERO','SALESIANOS','ESCUELA DE CIENCIAS SOCIALES'],
     'Servicios Socioculturales y a la Comunidad',
     'Técnico en Atención a Personas en Situación de Dependencia | '
     'Técnico Superior en Educación Infantil | '
     'Técnico Superior en Integración Social | '
     'Técnico Superior en Animación Sociocultural y Turística',
     'CFGM|CFGS'),

    (['DEPORTIV','DEPORTE','ACTIVIDADES FISICAS','ACTIVIDADES FÍSICAS','ACADEF',
      'LA OTRA FP_SPORT','FITNESS','ENTRENAMI'],
     'Actividades Físicas y Deportivas',
     'Técnico en Conducción de Actividades Físico-Deportivas en el Medio Natural | '
     'Técnico Superior en Acondicionamiento Físico | '
     'Técnico Superior en Enseñanza y Animación Sociodeportiva',
     'CFGM|CFGS'),

    (['MARKETING','COMERCIO','VENTAS','MODA','RETAIL','SUMA & MAS','SUMA & MÁS',
      'ESCUELA SUPERIOR DE SECRETARIAS','PROTOCOLO','ISEMCO','EVENTO','EVENT-FORM'],
     'Comercio y Marketing',
     'Técnico en Actividades Comerciales | '
     'Técnico Superior en Gestión de Ventas y Espacios Comerciales | '
     'Técnico Superior en Marketing y Publicidad | Técnico Superior en Comercio Internacional',
     'CFGM|CFGS'),

    (['ELECTRIC','ELECTRONICA','ELECTRÓNICA','AUTOMATI','AUTOMATIZ','ROBOTIC','MECATRONI'],
     'Electricidad y Electrónica',
     'Técnico en Instalaciones Eléctricas y Automáticas | '
     'Técnico Superior en Automatización y Robótica Industrial | '
     'Técnico Superior en Sistemas Electrotécnicos y Automatizados',
     'CFGM|CFGS'),

    (['CONSTRUCCION','CONSTRUCCIÓN','EDIFICACION','EDIFICACIÓN','OBRA CIVIL',
      'FUNDACION LABORAL DE LA CONSTRUCCION'],
     'Edificación y Obra Civil',
     'Técnico en Obras de Interior, Decoración y Rehabilitación | '
     'Técnico Superior en Proyectos de Edificación',
     'CFGM|CFGS'),

    (['AUTOMOCION','AUTOMOCIÓN','VEHICULOS','VEHÍCULOS','AVIATION','AERONAUT',
      'CARS MAROBE','TRAINEK'],
     'Transporte y Mantenimiento de Vehículos',
     'Técnico en Mantenimiento de Vehículos | Técnico Superior en Automoción | '
     'Técnico Superior en Mantenimiento Aeromecánico',
     'CFGM|CFGS'),

    (['ARTES GRAFICAS','ARTES GRÁFICAS','GRAFICO','GRÁFICO','DISEÑO','DISENO',
      'ARTE DIGITAL','ESDIP','GRAFTON','U-TAD','VOXEL SCHOOL'],
     'Artes Gráficas',
     'Técnico en Impresión Gráfica | '
     'Técnico Superior en Diseño y Gestión de la Producción Gráfica | '
     'Técnico Superior en Diseño y Edición de Publicaciones',
     'CFGM|CFGS'),

    (['AGRARI','AGROFORESTAL','AGRICOLA','AGRÍCOLA','EFA VALDEMILANOS',
      'JARDINERIA','JARDINERÍA','MEDIOAMBIENTE','MEDIO AMBIENTE'],
     'Agraria',
     'Técnico en Producción Agroecológica | '
     'Técnico Superior en Gestión Forestal y del Medio Natural | '
     'Técnico en Jardinería y Floristería',
     'CFGM|CFGS'),

    (['SEGURIDAD','EMERGENCIAS','BOMBEROS','POLICIA','POLICÍA','VIGILANCIA',
      'PROTECCION CIVIL','IFP VIGILES','GRUPO AULA FORMACIÓN Y EMERGENCIAS',
      'INSTITUTO DE FORMACION PROFESIONAL DE SANIDAD Y EMERGENCIAS'],
     'Seguridad y Medio Ambiente',
     'Técnico Superior en Coordinación de Emergencias y Protección Civil | '
     'Técnico en Emergencias Sanitarias',
     'CFGM|CFGS'),
]


def _inferir_fp(nombre):
    """Devuelve (familia, especialidad, enseñanza) inferidas del nombre del centro."""
    nombre_up = str(nombre).upper()
    for keywords, familia, ciclos, ens in KEYWORD_MAP:
        if any(kw in nombre_up for kw in keywords):
            return familia, ciclos, ens
    return None, None, None


def _enriquecer(df):
    """Rellena familia_fp, especialidad, enseñanzas y curso_academico."""
    familias, especialidades, ensenanzas, cursos = [], [], [], []

    for _, row in df.iterrows():
        tipo   = str(row['tipo']).strip()
        nombre = str(row['nombre']).strip()
        familia, ciclos, ens = _inferir_fp(nombre)

        if tipo == 'IES':
            base = 'ESO|Bachillerato'
            familias.append(familia or 'Múltiples familias')
            especialidades.append(ciclos or 'ESO | Bachillerato | Ciclos Formativos de GM y GS')
            ensenanzas.append(f'{base}|{ens}' if ens else f'{base}|CFGM|CFGS')
        elif tipo in ('CIFP', 'CP IFP'):
            familias.append(familia or 'Múltiples familias')
            especialidades.append(ciclos or 'Ciclos Formativos de Grado Medio y Superior')
            ensenanzas.append(f'FP Básica|{ens}' if ens else 'FP Básica|CFGM|CFGS')
        else:   # CPR FPE, CP FPE …
            familias.append(familia or 'Administración y Gestión')
            especialidades.append(
                ciclos or 'Técnico Superior en Administración y Finanzas | '
                          'Técnico en Gestión Administrativa'
            )
            ensenanzas.append(ens or 'CFGM|CFGS')

        cursos.append('2024-25')

    df = df.copy()
    df['familia_fp']      = familias
    df['especialidad']    = especialidades
    df['enseñanzas']      = ensenanzas
    df['curso_academico'] = cursos
    return df


# ─────────────────────────────────────────────────────────────────────────────
# CARGA Y LIMPIEZA
# ─────────────────────────────────────────────────────────────────────────────

def limpiar_datos():
    print("Cargando y limpiando datos...")

    # ── Intentar cargar ya el CSV limpio y enriquecido ────────────────────────
    if os.path.exists(RUTA_LIMPIO):
        df = pd.read_csv(RUTA_LIMPIO)
        # Comprobar si ya tiene datos en las columnas clave
        cols_ok = ['enseñanzas', 'especialidad', 'familia_fp', 'curso_academico']
        if all(col in df.columns for col in cols_ok):
            vacios = sum(df[c].isna().all() or (df[c] == '').all() for c in cols_ok)
            if vacios == 0:
                print(f"CSV limpio ya enriquecido cargado ({len(df)} registros).\n")
                return df

    # ── Si no hay CSV limpio, regenerar desde el origen ──────────────────────
    if not os.path.exists(RUTA_ORIGEN):
        print(f"[!] No se encuentra '{RUTA_ORIGEN}'. "
              f"Coloca el archivo en la ruta indicada y vuelve a ejecutar.")
        sys.exit()

    df = pd.read_csv(RUTA_ORIGEN)
    print(f"Total de registros iniciales: {len(df)}")

    tipos_ies_fp = ['IES', 'CIFP', 'CPR FP', 'CPR FPE', 'IFP', 'SFP', 'CFP', 'CP FPE', 'CP IFP']
    df = df[df['tipo'].isin(tipos_ies_fp)].copy()
    df = df.dropna(subset=['latitud', 'longitud'])
    print(f"Registros tras filtrado: {len(df)}")

    # ── Enriquecer columnas vacías ────────────────────────────────────────────
    print("Enriqueciendo enseñanzas, especialidades y familias FP...")
    df = _enriquecer(df)

    os.makedirs(os.path.dirname(RUTA_LIMPIO), exist_ok=True)
    df.to_csv(RUTA_LIMPIO, index=False, encoding='utf-8')
    print(f"Archivo exportado como {RUTA_LIMPIO}.\n")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_graficos(df):
    print("\nGenerando gráficos... Cierra la ventana para volver al menú.")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.countplot(
        data=df, x='titularidad', hue='titularidad',
        palette='viridis', legend=False, ax=axes[0]
    )
    axes[0].set_title('Distribución de IES y FP por Titularidad')
    axes[0].set_xlabel('Titularidad')
    axes[0].set_ylabel('Cantidad de Centros')

    top_municipios = df['municipio'].value_counts().head(10)
    sns.barplot(
        y=top_municipios.index, x=top_municipios.values,
        hue=top_municipios.index, palette='magma', legend=False, ax=axes[1]
    )
    axes[1].set_title('Top 10 Municipios con más IES y Centros de FP')
    axes[1].set_xlabel('Número de Institutos')
    axes[1].set_ylabel('Municipio')

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# BÚSQUEDA
# ─────────────────────────────────────────────────────────────────────────────

def buscar_por_ciclo(df):
    ciclo = input(
        "\nIntroduce el nombre o palabra clave "
        "(ej. 'Informática', 'Sanidad', 'Administración', 'Deporte'): "
    ).strip()

    cols = ['enseñanzas', 'especialidad', 'familia_fp']
    mascara = pd.Series(False, index=df.index)
    for col in cols:
        if col in df.columns:
            mascara |= df[col].fillna('').str.contains(ciclo, case=False, regex=False)

    resultados = df[mascara]

    if resultados.empty:
        print(f"\nNo se encontraron centros con '{ciclo}'.")
        print("Sugerencias de búsqueda: Informática, Sanidad, Administración, "
              "Hostelería, Deporte, Social, Marketing, Imagen Personal, Electricidad")
    else:
        cols_mostrar = ['nombre', 'tipo', 'municipio', 'titularidad', 'familia_fp', 'enseñanzas']
        print(f"\n--- {len(resultados)} centros encontrados para '{ciclo}' ---")
        print(resultados[cols_mostrar].head(20).to_string(index=False))
        if len(resultados) > 20:
            print(f"... y {len(resultados) - 20} resultados más.")


# ─────────────────────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def menu_principal():
    df = limpiar_datos()

    while True:
        print("\n" + "=" * 45)
        print("   MENÚ DE GESTIÓN DE INSTITUTOS FP/IES")
        print("=" * 45)
        print("1. Mostrar gráficos de distribución")
        print("2. Buscar institutos por ciclo/enseñanza")
        print("3. Salir")
        print("=" * 45)

        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == '1':
            mostrar_graficos(df)
        elif opcion == '2':
            buscar_por_ciclo(df)
        elif opcion == '3':
            print("\n¡Hasta pronto!")
            sys.exit()
        else:
            print("\n[!] Opción no válida. Elige 1, 2 o 3.")


if __name__ == "__main__":
    menu_principal()
