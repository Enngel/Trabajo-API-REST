import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from api.models import Instituto

class Command(BaseCommand):
    help = 'Carga institutos desde data/dataset_madrid.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default=os.path.join('data', 'dataset_madrid.csv'),
            help='Ruta al CSV (por defecto: data/dataset_madrid.csv)',
        )

    def handle(self, *args, **options):
        csv_path = options['csv']
        if not os.path.exists(csv_path):
            raise CommandError(f"Archivo no encontrado: {csv_path}")

        self.stdout.write(f"Leyendo: {csv_path}")
        df = pd.read_csv(csv_path, encoding='utf-8')

        creados = actualizados = 0
        for _, row in df.iterrows():
            _, created = Instituto.objects.update_or_create(
                nombre=str(row.get('nombre', '')).strip(),
                defaults={
                    'municipio':     row.get('municipio', ''),
                    'distrito':      row.get('distrito', ''),
                    'direccion':     row.get('direccion', ''),
                    'codigo_postal': str(row.get('codigo_postal', '')),
                    'titularidad':   row.get('titularidad', ''),
                    'telefono':      str(row.get('telefono', '')),
                    'email':         row.get('email', ''),
                    'web':           row.get('web', ''),
                    'latitud':       row.get('latitud')  if pd.notna(row.get('latitud'))  else None,
                    'longitud':      row.get('longitud') if pd.notna(row.get('longitud')) else None,
                }
            )
            if created: creados += 1
            else:       actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Carga completa — Creados: {creados} | Actualizados: {actualizados}"
        ))
