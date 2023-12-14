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
        if borrowing.actual_return:
            return Response(
                {"error": "The borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return = timezone.now().date()

        book = borrowing.book_id
        book.inventory += 1

        book.save()
        borrowing.save()

        return Response(
            {"message": "Borrowing returned successfully."},
            status=status.HTTP_200_OK
        )
