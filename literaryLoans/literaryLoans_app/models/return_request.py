from django.db import models

class ReturnRequest(models.Model):
    request_id = models.SmallIntegerField(default=0)
    borrower_id = models.SmallIntegerField(default=0)
    lender_id = models.SmallIntegerField(default=0)
    book_id = models.SmallIntegerField(default=0)
    status = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    request_date = models.DateField(auto_now_add=True)