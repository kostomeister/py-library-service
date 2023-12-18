from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from book_service.models import Book
from borrowing_service.models import Borrowing
from notifications.messages import successful_payment_message, successful_fine_payment_message
from payment_service.models import Payment
from payment_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from payment_service.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows listing and retrieving payments.
    """

    queryset = Payment.objects.select_related("borrowing").order_by(
        "borrowing__borrow_date"
    )
    serializer_class = PaymentSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        """
        Get the queryset of payments based on user role.

        For admins, all payments are retrieved.
        For regular users, only their payments are retrieved.

        Returns:
        - queryset: Filtered queryset based on user's role.
        """
        queryset = self.queryset

        if self.action == "list":
            if not self.request.user.is_staff:
                queryset = queryset.filter(borrowing_id__user_id=self.request.user)

        if self.action == "retrieve":
            queryset = queryset.order_by("borrowing__borrow_date")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer

        elif self.action == "retrieve":
            return PaymentDetailSerializer

        return PaymentSerializer


class SuccessView(APIView):
    """
    API endpoint for processing successful regular payments.
    """

    def get(self, request, borrowing_id):
        borrowing = Borrowing.objects.get(id=borrowing_id)
        payment = Payment.objects.get(borrowing=borrowing)

        payment.status = Payment.StatusChoices.PAID
        payment.money_to_pay = 0
        payment.save()

        book = Book.objects.get(borrowings=borrowing_id)
        book.inventory -= 1
        book.save()

        successful_payment_message(borrowing)

        return Response(
            {"message": "Payment was successfully processed"}, status=status.HTTP_200_OK
        )


class SuccessFineView(APIView):
    """
    API endpoint for processing successful fine payments.
    """

    def get(self, request, borrowing_id):
        borrowing = Borrowing.objects.get(id=borrowing_id)

        payment = Payment.objects.get(
            borrowing=borrowing, type=Payment.TypeChoices.FINE
        )

        payment.status = Payment.StatusChoices.PAID
        payment.type = Payment.TypeChoices.PAYMENT
        payment.money_to_pay = 0
        payment.save()

        book = Book.objects.get(borrowings=borrowing_id)
        book.inventory += 1
        book.save()

        successful_fine_payment_message(borrowing)

        return Response(
            {"message": "Payment for FINE was successfully processed"},
            status=status.HTTP_200_OK,
        )


class CancelView(APIView):
    """
    API endpoint for cancelling payment.
    """

    def get(self, request, borrowing_id):
        return Response(
            {"message": "Payment can be paid later"}, status=status.HTTP_400_BAD_REQUEST
        )
