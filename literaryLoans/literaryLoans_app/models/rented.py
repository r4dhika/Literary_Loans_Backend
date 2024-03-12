from django.db import models

class Rented(models.Model):
    rent_id = models.SmallIntegerField()
    borrower_id = models.SmallIntegerField()
    book_id = models.SmallIntegerField()
    quantity = models.IntegerField()
    rent_date = models.DateField()
    return_date = models.DateField()