from django.db import models

class CicloFormativo(models.Model):
    # Usamos un slug o código si existiera, si no, AutoField
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Ciclo")
    familia_profesional = models.CharField(max_length=150, verbose_name="Familia Profesional")
    grado = models.CharField(max_length=100, verbose_name="Grado (Medio/Superior)")

    class Meta:
        verbose_name = "Ciclo Formativo"
        verbose_name_plural = "Ciclos Formativos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.grado})"

class Instituto(models.Model):
    # Usamos el código del CSV como PK
    codigo = models.IntegerField(primary_key=True, verbose_name="Código de Centro")
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, help_text="Ej: IES, CPR FPE")
    titularidad = models.CharField(max_length=100)
    municipio = models.CharField(max_length=150)
    direccion = models.CharField(max_length=300)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    web = models.URLField(max_length=500, null=True, blank=True)
    
    # Coordenadas
    latitud = models.FloatField()
    longitud = models.FloatField()
    
    # Estado
    situacion = models.CharField(max_length=50, default="ALTA")
    
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

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"