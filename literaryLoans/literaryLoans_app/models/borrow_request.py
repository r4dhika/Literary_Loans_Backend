from django.db import models
import datetime

class BorrowRequest(models.Model):
    stat = [
        ('0', 'pending'),
        ('1', 'accepted'),
        ('2', 'rejected')
    ]
    request_id = models.SmallIntegerField(default=0)
    borrower_id = models.SmallIntegerField(default=0)
    lender_id = models.SmallIntegerField(default=0)
    book_id = models.SmallIntegerField(default=0)
    status = models.CharField(max_length=1, choices=stat, default='0')
    quantity = models.IntegerField(default=0)
    request_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(default=datetime.date.today)