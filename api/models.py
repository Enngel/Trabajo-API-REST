from django.db import models

class CicloFormativo(models.Model):
    # Usamos un slug o código si existiera, si no, AutoField
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Ciclo", db_index=True)
    abreviacion = models.CharField(
        max_length=10,
        verbose_name="Abreviación (ej: DAW, ASIR)",
        blank=True,
        null=True,
        db_index=True,
        help_text="Código corto para búsqueda rápida"
    )
    familia_profesional = models.CharField(max_length=150, verbose_name="Familia Profesional", db_index=True)
    grado = models.CharField(max_length=100, verbose_name="Grado (Medio/Superior)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Ciclo Formativo"
        verbose_name_plural = "Ciclos Formativos"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['abreviacion']),
            models.Index(fields=['familia_profesional']),
        ]

    def __str__(self):
        abrev = f" ({self.abreviacion})" if self.abreviacion else ""
        return f"{self.nombre}{abrev} - {self.grado}"

class Instituto(models.Model):
    # Usamos el código del CSV como PK
    codigo = models.IntegerField(primary_key=True, verbose_name="Código de Centro")
    nombre = models.CharField(max_length=255, db_index=True)
    tipo = models.CharField(max_length=50, help_text="Ej: IES, CPR FPE", db_index=True)
    titularidad = models.CharField(max_length=100, db_index=True)
    municipio = models.CharField(max_length=150, db_index=True)
    distrito = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    direccion = models.CharField(max_length=300)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    web = models.URLField(max_length=500, null=True, blank=True)
    
    # Coordenadas para geolocalización
    latitud = models.FloatField()
    longitud = models.FloatField()
    
    # Estado
    situacion = models.CharField(max_length=50, default="ALTA")
    
    # Campos adicionales para búsqueda
    keywords = models.TextField(
        blank=True,
        null=True,
        verbose_name="Palabras clave (búsqueda)",
        help_text="Separadas por comas. Ej: informática, programación, desarrollo"
    )

    # Relación ManyToMany
    ciclos = models.ManyToManyField(
        CicloFormativo, 
        related_name="institutos",
        blank=True,
        verbose_name="Ciclos que imparte"
    )

    class Meta:
        verbose_name = "Instituto"
        verbose_name_plural = "Institutos"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['municipio']),
            models.Index(fields=['tipo']),
            models.Index(fields=['latitud', 'longitud']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_distance_to(self, lat, lon):
        """Calcula distancia a coordenadas usando Haversine (aproximado en km)"""
        from math import radians, cos, sin, asin, sqrt

        lon1, lat1, lon2, lat2 = map(radians, [self.longitud, self.latitud, lon, lat])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
