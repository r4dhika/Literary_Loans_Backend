# urls.py

from django.urls import path
from literaryLoans_app import views

urlpatterns = [
    # Define the URL pattern for retrieving user addresses
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request'),
    path('books/delete/<int:id>/', views.BookDestroyAPIView.as_view(), name = 'book Delete'),
    path('borrowedbooks/<int:user_id>/', views.BorrowedbooksListAPIView.as_view(), name = 'Borrowed Books'),
    path('lendedbooks/<int:user_id>/', views.LendedbooksListAPIView.as_view(), name = 'Lended Books'),
    path('requestedbooks/<int:user_id>/', views.RequestedbooksListAPIView.as_view(), name = 'Requested Books'),
    path('address/<int:user_id>/', views.user_addresses, name='User Address'),
    path('destinations/<int:user_id>/', views.UserDestinations.as_view(), name='User Destinations'),
    path('calculateDistance/', views.CalculateDistance.as_view(), name = 'Estimated Distances'),
    path('auth/google/token/', views.google_token, name="login-with-google"),
    path('borrowRequests/<int:user_id>/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request'),
    path('auth/data/', views.user_data, name="user data"),
    path('profile/<int:id>/', views.UserDetailAPIView.as_view(), name = "Profile"),
    path('onboard/', views.onboarding, name = "onboarding"),
    path('book/create/', views.createBook, name = "Book Create"),
    path('lender_return/', views.lender_return, name='lender-return'),
    path('accept_return_request/', views.accept_return_request, name='accept-return-request'),
    path('create_return_request/', views.create_return_request, name='create-return-request'),
]