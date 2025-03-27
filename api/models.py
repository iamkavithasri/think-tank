# api/models.py

# api/models.py
from django.db import models

class CarAttributes(models.Model):
    wheel_size = models.IntegerField()      # Wheel size field
    grille_type = models.CharField(max_length=50)  # Grille type field
    fuel_type = models.CharField(max_length=50)    # Fuel type field
    color = models.CharField(max_length=50)       # Color field
    body_type = models.CharField(max_length=50)   # Body type field

    def __str__(self):
        return f"Wheel Size: {self.wheel_size}, Grille Type: {self.grille_type}, Fuel Type: {self.fuel_type}, Color: {self.color}, Body Type: {self.body_type}"
