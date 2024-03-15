from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookGenre)
admin.site.register(BorrowRequest)
admin.site.register(Genre)
admin.site.register(Rented)
admin.site.register(ReturnRequest)
