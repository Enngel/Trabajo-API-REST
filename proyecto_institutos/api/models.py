from django.db import models

class Instituto(models.Model):
    nombre        = models.CharField(max_length=255)
    municipio     = models.CharField(max_length=100, blank=True)
    distrito      = models.CharField(max_length=100, blank=True)
    direccion     = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=10,  blank=True)
    titularidad   = models.CharField(max_length=50,  blank=True)
    telefono      = models.CharField(max_length=20,  blank=True)
    email         = models.EmailField(blank=True)
    web           = models.URLField(blank=True)
    latitud       = models.FloatField(null=True, blank=True)
    longitud      = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Institutos'
        ordering = ['municipio', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.municipio})"
