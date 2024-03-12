from django.db import models

class Address(models.Model):
    pincode = models.BigIntegerField(default = 0)
    city = models.CharField(default = '', max_length = 255)
    country = models.CharField(default = '', max_length = 255)
