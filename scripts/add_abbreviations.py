"""
Script para actualizar ciclos formativos con abreviaciones
Ejecutar: python manage.py shell < scripts/add_abbreviations.py
"""

from api.models import CicloFormativo

# Mapeo de ciclos comunes con sus abreviaciones
CICLOS_ABREVIATURAS = {
    'Desarrollo de Aplicaciones Web': 'DAW',
    'Desarrollo de Aplicaciones Multiplataforma': 'DAM',
    'Administración de Sistemas Informáticos en Red': 'ASIR',
    'Técnico en Ciberseguridad en Entornos TI': 'CET',
    'Técnico en Administración de Bases de Datos': 'ABD',
    'Técnico en Gestión Administrativa': 'GA',
    'Técnico Superior en Administración y Finanzas': 'AF',
    'Técnico Superior en Asistencia a la Dirección': 'AD',
    'Técnico en Farmacia y Parafarmacia': 'FP',
    'Técnico en Cuidados Auxiliares de Enfermería': 'CAE',
    'Técnico Superior en Laboratorio Clínico y Biomédico': 'LCB',
    'Técnico Superior en Sonido e Iluminación': 'SI',
    'Técnico en Gestión de Alojamientos Turísticos': 'GAT',
    'Técnico en Cocina': 'CO',
    'Técnico en Servicios de Restauración': 'SR',
    'Técnico en Electricidad y Electrónica': 'EE',
    'Técnico en Instalaciones Frigoríficas': 'IF',
    'Técnico en Mecanizado': 'ME',
    'Técnico en Soldadura': 'SO',
    'Técnico en Construcción': 'CON',
    'Técnico en Carpintería': 'CAR',
    'Técnico en Soldadura y Calderería': 'SC',
    'Técnico en Fabricación y Montaje de Estructuras Metálicas': 'FM',
    'Técnico Superior en Automoción': 'AU',
    'Técnico en Mantenimiento de Vehículos': 'MV',
    'Técnico en Transporte Marítimo y Gestión del Buque': 'TM',
    'Técnico en Agricultura': 'AG',
    'Técnico en Ganadería y Asistencia Ganadera': 'GA',
    'Técnico en Jardinería': 'JA',
    'Técnico en Viticultura y Enología': 'VE',
}

def add_abbreviations():
    """Añade abreviaciones a los ciclos existentes"""
    updated = 0
    not_found = 0

    for nombre_ciclo, abreviacion in CICLOS_ABREVIATURAS.items():
        try:
            ciclos = CicloFormativo.objects.filter(nombre__icontains=nombre_ciclo[:15])
            if ciclos.exists():
                for ciclo in ciclos:
                    if not ciclo.abreviacion:
                        ciclo.abreviacion = abreviacion
                        ciclo.save()
                        print(f"✓ {ciclo.nombre} → {abreviacion}")
                        updated += 1
            else:
                print(f"⚠ No encontrado: {nombre_ciclo}")
                not_found += 1
        except Exception as e:
            print(f"✗ Error con {nombre_ciclo}: {e}")

    print(f"\n═════════════════════════════════════")
    print(f"Actualizados: {updated}")
    print(f"No encontrados: {not_found}")
    print(f"═════════════════════════════════════")

if __name__ == '__main__':
    add_abbreviations()

