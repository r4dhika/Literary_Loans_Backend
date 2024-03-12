from django.db import models

class ReturnRequest(models.Model):
    request_id = models.SmallIntegerField()
    borrower_id = models.SmallIntegerField()
    lender_id = models.SmallIntegerField()
    book_id = models.SmallIntegerField()
    status = models.BooleanField()
    quantity = models.IntegerField()
    request_date = models.DateField()