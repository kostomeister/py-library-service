from rest_framework import serializers
from book_service.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "inventory", "daily_fee")


class BookDetailSerializer(BookSerializer):
    pass
