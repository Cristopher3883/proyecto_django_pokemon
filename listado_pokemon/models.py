from django.db import models

class Type(models.Model):
    nombre = models.CharField(max_length=50)
    img = models.URLField(null=True, blank=True) 

    def __str__(self):
        return self.nombre

class Pokemon(models.Model):
    nombre = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField(null=True, blank=True)
    types = models.ManyToManyField(Type, related_name="pokemons")
    img = models.URLField(null=True, blank=True) 

    # Relación de evoluciones (muchas a muchas consigo mismo)
    evoluciones = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='pre_evoluciones', 
        blank=True
    )

    def __str__(self):
        return self.nombre

    def nombre_formateado(self):
        return self.nombre.replace("-", " ").title()