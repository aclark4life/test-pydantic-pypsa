# Create your models here.
from django.db import models

class EnergySystem(models.Model):
    name = models.CharField(max_length=100)
    capacity_mw = models.FloatField()
    efficiency = models.FloatField()
    cost_per_mw = models.FloatField()
