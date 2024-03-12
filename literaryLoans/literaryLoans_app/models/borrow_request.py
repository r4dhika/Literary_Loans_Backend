from django.db import models

class BorrowRequest(models.Model):
    stat = [
        ('0', 'pending'),
        ('1', 'accepted'),
        ('2', 'rejected')
    ]
    request_id = models.SmallIntegerField()
    borrower_id = models.SmallIntegerField()
    lender_id = models.SmallIntegerField()
    book_id = models.SmallIntegerField()
    status = models.CharField(max_length=1, choices=stat, default='0')
    quantity = models.IntegerField()
    request_date = models.DateField()
    return_date = models.DateField()