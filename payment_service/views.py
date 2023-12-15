from rest_framework import mixins, viewsets

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
