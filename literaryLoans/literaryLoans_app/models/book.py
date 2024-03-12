from django.db import models

class Book(models.Model):
    stat = [
        ('0', 'available'),
        ('1', 'out of stock'),
    ]
    book_id = models.SmallIntegerField(default=0)
    title = models.CharField(default='', max_length=255)
    status = models.CharField(max_length=1, choices=stat, default='0')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lender_id = models.SmallIntegerField(default=0)
    quantity = models.IntegerField(default=0)
    author_id = models.SmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    book_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_book_rating = models.IntegerField(default=0)
    condition_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_condition_rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='book_images/')