from django.db import models
from .user import User

class Book(models.Model):
    stat = [
        ('0', 'available'),
        ('1', 'out of stock'),
    ]
    book_id = models.SmallIntegerField(default=0)
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='Description')
    status = models.CharField(max_length=1, choices=stat, default='0')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_lender")
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_borrower", null=True, blank=True)
    quantity = models.IntegerField(default=0)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    book_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_book_rating = models.IntegerField(default=0)
    condition_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_condition_rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='book_images/')