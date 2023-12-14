import datetime


def calculating_total_sum_for_begin_of_borrowing(
        daily_fee: float,
        expected_return: datetime) -> float:

    days_in_borrowing = expected_return - datetime.date.today()
    return round((days_in_borrowing.days + 1) * daily_fee, 2)


def calculating_sum_of_forfeit(daily_fee: float,
                               expected_return: datetime,
                               actual_return: datetime) -> float:
    forfeit_days = actual_return - expected_return
    return round(forfeit_days.days * daily_fee * 1.5, 2)
