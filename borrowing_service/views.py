import datetime

from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)
from payment_service.models import Payment
from payment_service.stripe_helper import create_fine_session


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "return":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not user.is_staff:
            queryset = queryset.filter(user_id=user)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active:
            queryset = queryset.filter(actual_return__isnull=True)

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        permission_classes=[IsAdminUser],
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return is not None:
            return Response(
                {"error": "You already have a link to pay the fine"
                          " or have successfully returned the book"},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return = datetime.date.today()
        borrowing.save()

        if borrowing.expected_return_date >= datetime.date.today():
            book = borrowing.book_id
            book.inventory += 1
            book.save()
            return Response(
                {"message": "The book was successfully returned!"},
                status=status.HTTP_200_OK
            )

        session = create_fine_session(borrowing, request)

        Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            type=Payment.TypeChoices.FINE,
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=session.amount_total / 100,
        )

        book = borrowing.book_id
        book.inventory += 1
        book.save()

        return Response(
            {"message": "You must pay the fine before returning the book."},
            status=status.HTTP_400_BAD_REQUEST
        )
