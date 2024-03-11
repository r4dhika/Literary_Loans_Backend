from django.db import models

class BorrowRequest(models.Model):
    request_id = models.SmallIntegerField()
    borrower_id = models.SmallIntegerField()
    book_id = models.SmallIntegerField()
    status = models.SmallIntegerField()
    quantity = models.IntegerField()
    request_date = models.DateField()
    return_date = models.DateField()