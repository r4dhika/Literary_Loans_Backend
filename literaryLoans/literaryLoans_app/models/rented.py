from django.db import models
import datetime
from .user import User
from .book import Book

class Rented(models.Model):
    rent_id = models.SmallIntegerField(default=0)
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender_rented_books")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower_rented_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rented_books")
    quantity = models.IntegerField(default=0)
    rent_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(default=datetime.date.today)
