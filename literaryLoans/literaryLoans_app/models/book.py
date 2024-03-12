from django.db import models

class Book(models.Model):
    stat = [
        ('0', 'available'),
        ('1', 'out of stock'),
    ]
    book_id = models.SmallIntegerField()
    title = models.CharField(default = '', max_length = 255)
    status = models.CharField(max_length=1, choices=stat, default='0')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    penalty = models.DecimalField(max_digits=10, decimal_places=2)
    lender_id = models.SmallIntegerField()
    quantity = models.IntegerField()
    author_id = models.SmallIntegerField()
    available = models.BooleanField()
    book_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_book_rating = models.IntegerField()
    condition_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_condition_rating = models.IntegerField()
    image = models.ImageField(upload_to='book_images/')