import datetime
from decimal import Decimal

FINE_MULTIPLIER = Decimal("1.5")


def calculating_total_sum_for_begin_of_borrowing(
    daily_fee: float, expected_return: datetime
) -> int:
    """
    Calculates the total sum for the beginning of borrowing.

    Args:
    - daily_fee (float): Daily fee for borrowing.
    - expected_return (datetime): Expected return date.

    Returns:
    - int: Total sum for the beginning of borrowing in cents.
    """
    days_in_borrowing = expected_return - datetime.date.today()
    return int((days_in_borrowing.days + 1) * daily_fee * 100)


def calculating_sum_of_fine(
    daily_fee: float, expected_return: datetime, actual_return: datetime
) -> int:
    """
    Calculates the sum of fine for late return of a book.

    Args:
    - daily_fee (float): Daily fee for borrowing.
    - expected_return (datetime): Expected return date.
    - actual_return (datetime): Actual return date.

    Returns:
    - int: Sum of fine for late return in cents.
    """
    fine_days = actual_return - expected_return
    return int(fine_days.days * daily_fee * FINE_MULTIPLIER * 100)
