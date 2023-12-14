from rest_framework import serializers

from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        )


class PaymentListSerializer(PaymentSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "money_to_pay"
        )


class PaymentDetailSerializer(PaymentSerializer):
    book = serializers.CharField(
        source="borrowing.book_id.title", read_only=True
    )
    return_date = serializers.CharField(
        source="borrowing.expected_return_date", read_only=True
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "return_date",
            "book",
            "money_to_pay",
            "session_url",
            "session_id"
        )
