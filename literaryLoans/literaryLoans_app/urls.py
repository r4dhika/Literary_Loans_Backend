# urls.py

from django.urls import path
from literaryLoans_app import views

urlpatterns = [
    # Define the URL pattern for retrieving user addresses
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request')
]