import os

from django.urls import reverse

from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

import stripe

from .calculation_of_the_amount_to_be_paid import calculating_total_sum_for_begin_of_borrowing
from .models import Borrowing

from payment_service.models import Payment
from payment_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from payment_service.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.select_related("borrowing").order_by("borrowing__borrow_date")
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":

            if not self.request.user.is_staff:
                queryset = queryset.filter(
                    borrowing_id__user_id=self.request.user
                )

        if self.action == "retrieve":
            queryset = queryset.order_by("borrowing__borrow_date")

        return queryset

    def get_serializer_class(self):

        if self.action == "list":
            return PaymentListSerializer

        elif self.action == "retrieve":
            return PaymentDetailSerializer

        return PaymentSerializer


stripe.api_key = os.environ.get("STRIPE_SECRET_API_KEY")


class PaymentCreateView(APIView):

    def post(self, request, borrowing_id):
        borrowing = Borrowing.objects.get(id=borrowing_id)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': borrowing.book_id.title,
                    },
                    'unit_amount': calculating_total_sum_for_begin_of_borrowing(
                        borrowing.book_id.daily_fee,
                        borrowing.expected_return_date
                    )
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse(
                    "payments:payment-success",
                    kwargs={"borrowing_id": borrowing.id}
                )
            ),
            cancel_url=request.build_absolute_uri(
                reverse(
                    "payments:payment-cancel",
                    kwargs={"borrowing_id": borrowing.id}
                )
            )
        )

        payment = Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            type=Payment.TypeChoices.PAYMENT,
            borrowing=borrowing,
            money_to_pay=borrowing.book_id.daily_fee,
            session_id=session.id,
            session_url=session.url
        )

        return Response({'session_id': session.id, 'session_url': session.url})


class SuccessView(APIView):

    def get(self, request, borrowing_id):
        payment = get_object_or_404(Payment, borrowing_id=borrowing_id)

        payment.status = Payment.StatusChoices.PAID
        payment.money_to_pay = 0
        payment.save()

        return Response({'message': 'Payment was successfully processed'}, status=status.HTTP_200_OK)


class CancelView(APIView):

    def get(self, request, borrowing_id):
        return Response({'message': 'Payment can be paid later'}, status=status.HTTP_400_BAD_REQUEST)
