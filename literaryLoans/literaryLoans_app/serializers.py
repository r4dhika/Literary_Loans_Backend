from  rest_framework  import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model=Book
        fields='__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        fields='__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model=Author
        fields='__all__'


class BookGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=BookGenre
        fields='__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=Genre
        fields='__all__'


class  BorrowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model=BorrowRequest
        fields='__all__'


class RentedSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rented
        fields='__all__'



