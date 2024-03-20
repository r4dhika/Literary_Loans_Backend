from  rest_framework  import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class BookSerializer(serializers.ModelSerializer):
    lender_id = UserSerializer()
    borrower_id = UserSerializer()

    class Meta:
        model=Book
        fields='__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id', 'addressLine1', 'addressLine2', 'city', 'state', 'country']


class BookGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=BookGenre
        fields='__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=Genre
        fields='__all__'


class BorrowRequestSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    lender = UserSerializer()
    borrower = UserSerializer()

    class Meta:
        model = BorrowRequest
        fields = ['id', 'borrower', 'lender', 'book', 'status', 'quantity', 'request_date', 'return_date']


class RentedSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model=Rented
        fields='__all__'

class ReturnRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model=ReturnRequest
        fields='__all__'


