from django.db import models
from .user import User
from .genre import Genre

class Book(models.Model):
    stat = [
        ('0', 'available'),
        ('1', 'out of stock'),
    ]
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='Description')
    status = models.CharField(max_length=1, choices=stat, default='0')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_lender")
    quantity = models.IntegerField(default=0)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    book_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_book_rating = models.IntegerField(default=0)
    condition_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_condition_rating = models.IntegerField(default=0)
    image = models.CharField(max_length=10000, default = '')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name="book_genre", null=True, blank=True)