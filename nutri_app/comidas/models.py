from django.db import models

from django.db import models

class Comida(models.Model):
    nombre = models.CharField(max_length=100)
    calorias = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.calorias} kcal"

