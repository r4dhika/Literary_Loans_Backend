from django.db import models
import datetime
from .user import User
from .book import Book

class BorrowRequest(models.Model):
    STATUSES = [
        ('0', 'Pending'),
        ('1', 'Accepted'),
        ('2', 'Rejected')
    ]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower_borrow_requests")
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender_borrow_requests")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_requests")
    status = models.CharField(max_length=1, choices=STATUSES, default='0')
    quantity = models.IntegerField(default=0)
    request_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(default=datetime.date.today)

