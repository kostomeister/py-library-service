import datetime
import os

import stripe
from django.db import transaction
from rest_framework import serializers
from django.utils import timezone

from dotenv import load_dotenv

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from payment_service.models import Payment
from payment_service.stripe_helper import create_initial_session
from user.serializers import UserSerializer

load_dotenv()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date", "book_id", "user_id"
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

    @transaction.atomic
    def create(self, validated_data):
        stripe.api_key = os.environ.get("STRIPE_SECRET_API_KEY")

        user = self.context["request"].user
        validated_data["user_id"] = user

        book_id = validated_data["book_id"].id
        book_instance = Book.objects.get(pk=book_id)
        book_instance.inventory -= 1
        book_instance.save()

        borrowing = Borrowing.objects.create(**validated_data)

        session = create_initial_session(borrowing, self.context["request"])

        Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            type=Payment.TypeChoices.PAYMENT,
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=session.amount_total / 100,
        )

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
            "user",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return")

    def validate(self, data):
        super().validate(data)

        borrowing = self.instance
        if borrowing.actual_return is None:
            raise serializers.ValidationError("Actual return date is required.")

        if borrowing.actual_return <= borrowing.expected_return_date:
            raise serializers.ValidationError("Actual return date must be later than expected return date.")

        return data
