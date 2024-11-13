from django.db import models
from django.contrib.auth.models import User

class Causa(models.Model):
    titulo = models.CharField(max_length = 200)
    descripcion = models.TextField()
    meta_recaudacion = models.DecimalField(max_digits = 10, decimal_places = 2)
    cantidad_recaudada = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    fecha_creacion = models.DateTimeField(auto_now_add = True)
    fecha_fin = models.DateField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'causas', null = True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo', 'id']  # Orden por defecto en el modelo

class Donacion(models.Model):
    causa = models.ForeignKey(Causa, on_delete = models.CASCADE, related_name = 'donaciones')
    cantidad = models.DecimalField(max_digits = 10, decimal_places = 2)
    fecha_donacion = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'donaciones', null = True)

    def __str__(self):
        return f"Donación de {self.cantidad} a {self.causa.titulo} por {self.user.username}"
