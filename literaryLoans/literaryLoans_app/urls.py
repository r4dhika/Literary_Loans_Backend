# urls.py

from django.urls import path
from literaryLoans_app import views

urlpatterns = [
    # Define the URL pattern for retrieving user addresses
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('borrowRequests/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request'),
    path('returnRequests/', views.ReturnRequestListAPIView.as_view(), name='Return Request'),
    path('borrowRequestStatus/', views.BorrowRequestStatusListAPIView.as_view(), name = 'Borrow Request Status'),
    path('books/delete/<int:id>/', views.BookDestroyAPIView.as_view(), name = 'book Delete'),
    path('borrowedbooks/', views.BorrowedbooksListAPIView.as_view(), name = 'Borrowed Books'),
    path('lendedbooks/', views.LendedbooksListAPIView.as_view(), name = 'Lended Books'),
    path('requestedbooks/<int:user_id>/', views.RequestedbooksListAPIView.as_view(), name = 'Requested Books'),
    path('address/<int:user_id>/', views.user_addresses, name='User Address'),
    path('destinations/<int:user_id>/', views.UserDestinations.as_view(), name='User Destinations'),
    path('calculateDistance/', views.CalculateDistance.as_view(), name = 'Estimated Distances'),
    path('auth/google/token/', views.google_token, name="login-with-google"),
    path('borrowRequests/', views.BorrowRequestListAPIView.as_view(), name='Borrow Request'),
    path('auth/data/', views.user_data, name="user data"),
    path('profile/<int:id>/', views.UserDetailAPIView.as_view(), name = "Profile"),
    path('onboard/', views.onboarding, name = "onboarding"),
    path('book/create/', views.createBook, name = "Book Create"),
    path('lender_return/', views.lender_return, name='lender-return'),
    path('accept_return_request/', views.accept_return_request, name='accept-return-request'),
    path('create_return_request/', views.create_return_request, name='create-return-request'),
    path('create_borrow_request/',views.createBorrowRequest,name='create-borrow-request'),
    path('accept_borrow_request/',views.acceptBorrowRequest,name='accept_borrow_request'),
    path('reject_borrow_request/',views.rejectBorrowRequest,name='reject_borrow_request'),
    path('logout/', views.Logout.as_view(), name = 'Logout'),
    path('genre/', views.GenreListAPIView.as_view(), name='Genre'),
    path('books/genre/<str:genre_id>/', views.BooksByGenreAPIView.as_view(), name='books-by-genre'),
    path('send-email/', views.EmailAPI),
]