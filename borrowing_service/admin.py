from django.contrib import admin

from borrowing_service.models import Borrowing


@admin.register(Borrowing)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "borrow_date",
        "expected_return_date",
        "actual_return",
        "book_id",
        "user_id",
    )
    list_filter = ("expected_return_date", "book_id", "user_id")
