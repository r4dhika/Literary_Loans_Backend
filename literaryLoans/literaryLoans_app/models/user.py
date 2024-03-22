from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gen = [
        ('f', 'female'),
        ('m', 'male'),
        ('n', 'prefer not to say')
    ]
    email = models.EmailField('email', unique = True)
    phone_no = models.CharField('Phone Number', max_length=10, null=True, blank=True)
    isOnboarded = models.BooleanField('isOnboarded',default=False)
    rating_asLender = models.DecimalField(max_digits=4, decimal_places = 3, null=True, blank=True)
    rating_asBorrower = models.DecimalField(max_digits=4, decimal_places = 3, null=True, blank=True)
    total_rating_asLender = models.IntegerField(null=True, blank=True)
    total_rating_asBorrower = models.IntegerField(null=True, blank=True)
    addressLine1 = models.CharField(max_length = 1024, null=True, blank=True)
    addressLine2 = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField('City', max_length=255, null=True, blank=True)
    state = models.CharField('State', max_length=255, null=True, blank=True)
    country = models.CharField('Country', max_length=255, null=True, blank=True)
    picture = models.CharField('Image',  max_length = 255, null=True, blank=True)
    password = models.CharField('Password', max_length = 255, null = True, blank = True)

    def __str__(self):
        return self.email
