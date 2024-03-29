from django.db import models

from book_service.models import Book
from django.contrib.auth import get_user_model


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    class Meta:
        ordering = ("-borrow_date",)

    def __str__(self):
        return f"Borrowing of {self.user_id.email} on {self.borrow_date}"
