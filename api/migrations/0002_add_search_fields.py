"""
Migración para agregar campos de búsqueda mejorada a los modelos
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # Agregar campos a CicloFormativo
        migrations.AddField(
            model_name='cicloformativo',
            name='abreviacion',
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text='Código corto para búsqueda rápida',
                max_length=10,
                null=True,
                verbose_name='Abreviación (ej: DAW, ASIR)'
            ),
        ),
        migrations.AddField(
            model_name='cicloformativo',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='cicloformativo',
            name='familia_profesional',
            field=models.CharField(
                db_index=True,
                max_length=150,
                verbose_name='Familia Profesional'
            ),
        ),
        migrations.AlterField(
            model_name='cicloformativo',
            name='nombre',
            field=models.CharField(
                db_index=True,
                max_length=255,
                verbose_name='Nombre del Ciclo'
            ),
        ),
        # Agregar campos a Instituto
        migrations.AddField(
            model_name='instituto',
            name='distrito',
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=150,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='instituto',
            name='keywords',
            field=models.TextField(
                blank=True,
                help_text='Separadas por comas. Ej: informática, programación, desarrollo',
                null=True,
                verbose_name='Palabras clave (búsqueda)'
            ),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='municipio',
            field=models.CharField(
                db_index=True,
                max_length=150
            ),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='nombre',
            field=models.CharField(
                db_index=True,
                max_length=255
            ),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='tipo',
            field=models.CharField(
                db_index=True,
                help_text='Ej: IES, CPR FPE',
                max_length=50
            ),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='titularidad',
            field=models.CharField(
                db_index=True,
                max_length=100
            ),
        ),
        # Agregar índices
        migrations.AddIndex(
            model_name='cicloformativo',
            index=models.Index(
                fields=['nombre'],
                name='api_ciclofo_nombre_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='cicloformativo',
            index=models.Index(
                fields=['abreviacion'],
                name='api_ciclofo_abrevia_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='cicloformativo',
            index=models.Index(
                fields=['familia_profesional'],
                name='api_ciclofo_familia_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='instituto',
            index=models.Index(
                fields=['nombre'],
                name='api_instituto_nombre_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='instituto',
            index=models.Index(
                fields=['municipio'],
                name='api_instituto_municipio_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='instituto',
            index=models.Index(
                fields=['tipo'],
                name='api_instituto_tipo_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='instituto',
            index=models.Index(
                fields=['latitud', 'longitud'],
                name='api_instituto_geo_idx'
            ),
        ),
    ]

