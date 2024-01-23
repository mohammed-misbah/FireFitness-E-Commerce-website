from django.db import models

# Create your models here.

class Productoffer(models.Model):
    product   = models.CharField(max_length=100)
    discount  = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

class Categoryoffer(models.Model):
    category  = models.CharField(max_length=100)
    discount  = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    