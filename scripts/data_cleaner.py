"""
SCRIPT 1: Data Cleaner (Data Cleaning & Enrichment)
=====================================================
Carga datos brutos (centros_merged.csv), filtra tipos IES/FP,
enriquece con familias profesionales y genera institutos_limpios.csv
"""

import pandas as pd
import numpy as np
import sys
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

INPUT_FILE = os.path.join(DATA_DIR, 'centros_merged.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'institutos_limpios.csv')

# Mapeado KEYWORDS → familia FP oficial (catálogo LOMLOE)
KEYWORD_MAP = [
    (['INFORMATICA','INFORMÁTICA','NUEVAS TECNOLOG','TECNOLOG','DIGITAL','CYBER','CIBER',
      'SOFTWARE','PROGRAMACION','PROGRAMACIÓN','DATOS','DATA','INTERNET','REDES','NETWORK',
      'UNIVERSOFT','MICROFORUM','CIBERNOS','VODAFONE','UDIMA','DIGITECH','CDM INFINIA',
      'WINTRAIN','CORE NETWORKS','CAMPUS FP VISTALEGRE','CAMPUS FP ALCALA DE HENARES IT'],
     'Informática y Comunicaciones',
     'Administración de Sistemas Informáticos en Red | Desarrollo de Aplicaciones Web | '
     'Desarrollo de Aplicaciones Multiplataforma | Ciberseguridad en Entornos TI'),

    (['SALUD','SANIDAD','SANITAR','MEDIC','BIOSANITARI','HOSPITAL','DENTAL','ENFERMERIA',
      'ENFERMERÍA','FARMACIA','LABORATORI','CLINICO','CLÍNICO','HUMANIZACION','GALENO',
      'XTART','MEDAC','SANITAS','BOBATH','CAMPUS DENTAL','GRUPO CTO','FORMA-T',
      'INGENIERIA CLINICA','CAMPUS FP SOCIOSANITARIO'],
     'Sanidad',
     'Técnico en Cuidados Auxiliares de Enfermería | Técnico Superior en Laboratorio Clínico '
     'y Biomédico | Técnico Superior en Imagen para el Diagnóstico | Técnico Superior en Salud Ambiental'),

    (['ADMINISTRACION','ADMINISTRACIÓN','GESTION','GESTIÓN','EMPRESARIAL','FINANCIER',
      'FINANZAS','NEGOCIOS','CAMARA DE COMERCIO','CENTRO DE ESTUDIOS FINANCIEROS','ALTA DIRECCION',
      'ESERP','ESIC','AEI BUSINESS','BUSINESS AND LANGUAGE','FORMACION COMERCIAL','IMF',
      'ADAMS FP','FP SUMMA','CEF','ABACO','CARDENAL CISNEROS','JOVELLANOS','FOMENTO'],
     'Administración y Gestión',
     'Técnico en Gestión Administrativa | Técnico Superior en Administración y Finanzas | '
     'Técnico Superior en Asistencia a la Dirección'),

    (['HOSTELERIA','HOSTELERÍA','TURISMO','GASTRONOMIA','GASTRONOMÍA','COCINA','CULINARI',
      'RESTAURACION','RESTAURACIÓN','C.D.TUR','SIMONE ORTEGA','ESCUELA DE LA VID',
      'ESC. HOSTELERIA','MOM CULINARY','ESATUR','CENTRO SUPERIOR DE HOSTELERIA'],
     'Hostelería y Turismo',
     'Técnico en Cocina y Gastronomía | Técnico Superior en Dirección de Cocina | '
     'Técnico Superior en Gestión de Alojamientos Turísticos | '
     'Técnico Superior en Agencias de Viajes y Gestión de Eventos'),

    (['IMAGEN Y SONIDO','AUDIOVISUAL','CINE','VIDEO','SONIDO','RADIO','TELEVISION',
      'RTVE','FOTOGRAFIA','FOTOGRAFÍA','PUBLICIDAD','PRENSA','CEV','CES IMAGEN',
      'VOXEL','TRAZOS','INFOGRAFIA','UDIT','IED MADRID','COMUNICACION AUDIOVISUAL',
      'CAMPUS FP ARGANDA'],
     'Comunicación, Imagen y Sonido',
     'Técnico Superior en Producción de Audiovisuales | '
     'Técnico Superior en Realización de Proyectos Audiovisuales | '
     'Técnico Superior en Imagen | Técnico Superior en Sonido para Audiovisuales'),

    (['PELUQUERIA','PELUQUERÍA','ESTETICA','ESTÉTICA','BELLEZA','NOVELLA','IMAGEN PERSONAL'],
     'Imagen Personal',
     'Técnico en Peluquería y Cosmética Capilar | '
     'Técnico Superior en Estética Integral y Bienestar | '
     'Técnico Superior en Asesoría de Imagen Personal y Corporativa'),

    (['SOCIAL','SOCIOSANIT','ATENCION PERSON','DEPENDENCIA','EDUCACION INFANTIL',
      'EDUCACIÓN INFANTIL','TOMILLO','FUNDACION TOMILLO','CRUZ ROJA','JUAN LUIS MARROQUIN',
      'RECURSOS COM.SORDA','CAMPUS FP FUNDACION APROCOR','JUAN XXIII','MURIALDO',
      'SAN JOSE OBRERO','SALESIANOS','ESCUELA DE CIENCIAS SOCIALES'],
     'Servicios Socioculturales y a la Comunidad',
     'Técnico en Atención a Personas en Situación de Dependencia | '
     'Técnico Superior en Educación Infantil | '
     'Técnico Superior en Integración Social | '
     'Técnico Superior en Animación Sociocultural y Turística'),

    (['DEPORTIV','DEPORTE','ACTIVIDADES FISICAS','ACTIVIDADES FÍSICAS','ACADEF',
      'LA OTRA FP_SPORT','FITNESS','ENTRENAMI'],
     'Actividades Físicas y Deportivas',
     'Técnico en Conducción de Actividades Físico-Deportivas en el Medio Natural | '
     'Técnico Superior en Acondicionamiento Físico | '
     'Técnico Superior en Enseñanza y Animación Sociodeportiva'),

    (['MARKETING','COMERCIO','VENTAS','MODA','RETAIL','SUMA & MAS','SUMA & MÁS',
      'ESCUELA SUPERIOR DE SECRETARIAS','PROTOCOLO','ISEMCO','EVENTO','EVENT-FORM'],
     'Comercio y Marketing',
     'Técnico en Actividades Comerciales | '
     'Técnico Superior en Gestión de Ventas y Espacios Comerciales | '
     'Técnico Superior en Marketing y Publicidad | Técnico Superior en Comercio Internacional'),

    (['ELECTRIC','ELECTRONICA','ELECTRÓNICA','AUTOMATI','AUTOMATIZ','ROBOTIC','MECATRONI'],
     'Electricidad y Electrónica',
     'Técnico en Instalaciones Eléctricas y Automáticas | '
     'Técnico Superior en Automatización y Robótica Industrial | '
     'Técnico Superior en Sistemas Electrotécnicos y Automatizados'),

    (['CONSTRUCCION','CONSTRUCCIÓN','EDIFICACION','EDIFICACIÓN','OBRA CIVIL',
      'FUNDACION LABORAL DE LA CONSTRUCCION'],
     'Edificación y Obra Civil',
     'Técnico en Obras de Interior, Decoración y Rehabilitación | '
     'Técnico Superior en Proyectos de Edificación'),

    (['AUTOMOCION','AUTOMOCIÓN','VEHICULOS','VEHÍCULOS','AVIATION','AERONAUT',
      'CARS MAROBE','TRAINEK'],
     'Transporte y Mantenimiento de Vehículos',
     'Técnico en Mantenimiento de Vehículos | Técnico Superior en Automoción | '
     'Técnico Superior en Mantenimiento Aeromecánico'),

    (['ARTES GRAFICAS','ARTES GRÁFICAS','GRAFICO','GRÁFICO','DISEÑO','DISENO',
      'ARTE DIGITAL','ESDIP','GRAFTON','U-TAD','VOXEL SCHOOL'],
     'Artes Gráficas',
     'Técnico en Impresión Gráfica | '
     'Técnico Superior en Diseño y Gestión de la Producción Gráfica | '
     'Técnico Superior en Diseño y Edición de Publicaciones'),

    (['AGRARI','AGROFORESTAL','AGRICOLA','AGRÍCOLA','EFA VALDEMILANOS',
      'JARDINERIA','JARDINERÍA','MEDIOAMBIENTE','MEDIO AMBIENTE'],
     'Agraria',
     'Técnico en Producción Agroecológica | '
     'Técnico Superior en Gestión Forestal y del Medio Natural | '
     'Técnico en Jardinería y Floristería'),

    (['SEGURIDAD','EMERGENCIAS','BOMBEROS','POLICIA','POLICÍA','VIGILANCIA',
      'PROTECCION CIVIL','IFP VIGILES','GRUPO AULA FORMACIÓN Y EMERGENCIAS',
      'INSTITUTO DE FORMACION PROFESIONAL DE SANIDAD Y EMERGENCIAS'],
     'Seguridad y Medio Ambiente',
     'Técnico Superior en Coordinación de Emergencias y Protección Civil | '
     'Técnico en Emergencias Sanitarias'),
]


def _inferir_fp(nombre):
    """Devuelve (familia, ciclos) inferidas del nombre del centro."""
    nombre_up = str(nombre).upper()
    for keywords, familia, ciclos in KEYWORD_MAP:
        if any(kw in nombre_up for kw in keywords):
            return familia, ciclos
    return None, None


def _enriquecer(df):
    """Rellena familia_fp y especialidad."""
    familias, especialidades = [], []

    for _, row in df.iterrows():
        tipo = str(row['tipo']).strip()
        nombre = str(row['nombre']).strip()
        familia, ciclos = _inferir_fp(nombre)

        if tipo == 'IES':
            familias.append(familia or 'Múltiples familias')
            especialidades.append(ciclos or 'ESO | Bachillerato | Ciclos Formativos de GM y GS')
        elif tipo in ('CIFP', 'CP IFP'):
            familias.append(familia or 'Múltiples familias')
            especialidades.append(ciclos or 'Ciclos Formativos de Grado Medio y Superior')
        else:
            familias.append(familia or 'Administración y Gestión')
            especialidades.append(
                ciclos or 'Técnico Superior en Administración y Finanzas | '
                          'Técnico en Gestión Administrativa'
            )

    df = df.copy()
    df['familia_fp'] = familias
    df['especialidad'] = especialidades
    return df


def main():
    print("=" * 70)
    print("SCRIPT 1: DATA CLEANER - Limpieza y enriquecimiento de datos")
    print("=" * 70)

    # Crear directorio de data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(INPUT_FILE):
        print(f"\n[!] Error: No se encuentra '{INPUT_FILE}'")
        print(f"    Coloca el archivo centros_merged.csv en: {DATA_DIR}")
        return False

    print(f"\n[*] Cargando datos desde: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    print(f"    Total de registros iniciales: {len(df)}")

    # Filtrar tipos IES/FP
    tipos_ies_fp = ['IES', 'CIFP', 'CPR FP', 'CPR FPE', 'IFP', 'SFP', 'CFP', 'CP FPE', 'CP IFP']
    df = df[df['tipo'].isin(tipos_ies_fp)].copy()
    print(f"    Registros tras filtro de tipo: {len(df)}")

    # Limpiar valores nulos en coordenadas
    df = df.dropna(subset=['latitud', 'longitud'])
    print(f"    Registros tras filtro de coordenadas: {len(df)}")

    # Enriquecer columnas
    print("\n[*] Enriqueciendo datos con familias FP y especialidades...")
    df = _enriquecer(df)

    # Guardar
    print(f"\n[*] Guardando archivo limpio y enriquecido...")
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"    Archivo exportado: {OUTPUT_FILE}")
    print(f"    Total de registros: {len(df)}")

    print("\n[✓] Data Cleaner completado exitosamente")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

