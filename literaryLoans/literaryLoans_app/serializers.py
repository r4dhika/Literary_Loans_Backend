from  rest_framework  import serializers
from .models import *

class UserSerializer(serializers.Modelserializer):
    class Meta:
        model=User
        field='__all__'

class BookSerializer(serializers.Modelserializers):

    class Meta:
        model=Book
        field='__all__'


class AddressSerializer(serializers.Modelserializers):

    class Meta:
        model=Address
        field='__all__'


class AuthorSerializer(serializers.Modelserializers):

    class Meta:
        model=Author
        field='__all__'


class BookGenreSerializer(serializers.Modelserializers):

    class Meta:
        model=BookGenre
        field='__all__'


class GenreSerializer(serializers.Modelserializers):

    class Meta:
        model=Genre
        field='__all__'


class  BorrowRequestSerializer(serializers.Modelserializers):

    class Meta:
        model=BorrowRequest
        field='__all__'


class RentedSerializer(serializers.Modelserializers):

    class Meta:
        model=Rented
        field='__all__'



