from django.db import models
import datetime

class Rented(models.Model):
    rent_id = models.SmallIntegerField(default=0)
    borrower_id = models.SmallIntegerField(default=0)
    lender_id = models.SmallIntegerField(default=0)
    book_id = models.SmallIntegerField(default=0)
    quantity = models.IntegerField(default=0)
    rent_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(default=datetime.date.today)