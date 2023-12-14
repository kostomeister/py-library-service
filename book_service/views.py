from rest_framework import viewsets
from book_service.models import Book
from book_service.permissions import IsAdminOrReadOnly
from book_service.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the books with filters"""
        title = self.request.query_params.get("title")
        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer
