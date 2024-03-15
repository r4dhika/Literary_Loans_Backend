# urls.py

from django.urls import path
from literaryLoans_app import views

urlpatterns = [
    # Define the URL pattern for retrieving user addresses
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request'),
    path('books/delete/<int:pk>/', views.BookDestroyAPIView.as_view(), name = 'book Delete'),
    path('borrowedbooks/<int:user_id>/', views.BorrowedbooksListAPIView.as_view(), name = 'Borrowed Books'),
    path('lendedbooks/<int:user_id>/', views.LendedbooksListAPIView.as_view(), name = 'Lended Books'),
    path('requestedbooks/<int:user_id>/', views.RequestedbooksListAPIView.as_view(), name = 'Requested Books'),
    path('address/<int:user_id>/', views.user_addresses, name='User Address'),
    path('destinations/<int:user_id>/', views.UserDestinations.as_view(), name='User Destinations'),
    path('calculateDistance/', views.CalculateDistance.as_view(), name = 'Estimated Distances'),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request')
]