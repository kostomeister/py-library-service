from rest_framework import serializers
from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return",
            "book_id",
            "user_id",
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book_id.title", read_only=True)
    user = serializers.CharField(source="user_id.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "book", "user")
