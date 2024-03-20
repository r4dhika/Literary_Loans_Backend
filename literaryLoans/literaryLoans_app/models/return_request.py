from django.db import models
from .user import User
from .book import Book
from .rented import Rented
import datetime

class ReturnRequest(models.Model):
    STATUSES = [
        ('0', 'Pending'),
        ('1', 'Accepted')
    ]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="return_requests_as_borrower")
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="return_requests_as_lender")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="return_requests")
    status = models.CharField(max_length=1, choices=STATUSES, default='0')
    quantity = models.IntegerField(default=0)
    request_date = models.DateField(default=datetime.date.today)
    rented_id = models.ForeignKey(Rented, on_delete=models.CASCADE, related_name="rented", null=True, blank=True)
