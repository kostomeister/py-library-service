from rest_framework import serializers
from django.utils import timezone

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book_id",
            "user_id"
        )
        read_only_fields = ("user_id",)

    def validate(self, data):
      
        super().validate(data)
        
        book_id = data["book_id"].id
        book = Book.objects.get(pk=book_id)
        
        expected_return_date = data["expected_return_date"]
        current_time = timezone.now()

        if book.inventory < 1:
            raise serializers.ValidationError(
                "This book is not available for borrowing now"
            )

        if expected_return_date < current_time.date():
            raise serializers.ValidationError(
                "Expected return date cannot be in the past."
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user_id"] = user

        book_id = validated_data["book_id"].id
        book_instance = Book.objects.get(pk=book_id)
        book_instance.inventory -= 1
        book_instance.save()
        
        borrowing = Borrowing.objects.create(**validated_data)
        
        return borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book_id.title", read_only=True)
    user = serializers.CharField(source="user_id.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "book", "user")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user_id", read_only=True)
    book = BookSerializer(source="book_id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return",
            "book",
            "user"
        )
