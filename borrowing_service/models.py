from django.db import models

from book_service.models import Book
from config import settings


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowing")
    user_id = models.ForeignKey(
        settings.dev.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    class Meta:
        ordering = ("-borrow_date",)

    def __str__(self):
        return f"Borrowing of {self.book_id.title} on {self.borrow_date}"
