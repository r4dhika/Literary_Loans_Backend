from  rest_framework  import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        field='__all__'

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model=Book
        field='__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        field='__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model=Author
        field='__all__'


class BookGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=BookGenre
        field='__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=Genre
        field='__all__'


class  BorrowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model=BorrowRequest
        field='__all__'


class RentedSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rented
        field='__all__'



