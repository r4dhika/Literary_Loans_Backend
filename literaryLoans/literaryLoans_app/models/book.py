from django.db import models

class Book(models.model):
    book_id = models.SmallIntegerField()
    title = models.CharField(default = '', max_length = 255)
    status = models.TextField(default='', max_length=1023)
    status = models.SmallIntegerField()
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