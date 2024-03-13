# urls.py

from django.urls import path
from literaryLoans_app import views

urlpatterns = [
    # Define the URL pattern for retrieving user addresses
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('address/<int:user_id>/', views.user_addresses, name='User Address'),
    path('destinations/<int:user_id>/', views.UserDestinations.as_view(), name='User Destinations'),
    path('calculateDistance/', views.CalculateDistance.as_view(), name = 'Estimated Distances'),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request')
]