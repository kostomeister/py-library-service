import os

import stripe
from django.urls import reverse

from payment_service.calculation_of_the_amount_to_be_paid import (
    calculating_total_sum_for_begin_of_borrowing,
    calculating_sum_of_fine
)
from dotenv import load_dotenv

load_dotenv()


stripe.api_key = os.environ.get("STRIPE_SECRET_API_KEY")


def create_initial_session(borrowing, request):
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
    return session

# TODO implement fine stripe session

#
# def create_fine_session(borrowing, request):
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': "Fine for overdue of " + borrowing.book_id.title,
#                 },
#                 'unit_amount': calculating_total_sum_for_begin_of_borrowing(
#                     borrowing.book_id.daily_fee,
#                     borrowing.expected_return_date
#                 )
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=request.build_absolute_uri(
#             reverse(
#                 "payments:payment-success",
#                 kwargs={"borrowing_id": borrowing.id}
#             )
#         ),
#         cancel_url=request.build_absolute_uri(
#             reverse(
#                 "payments:payment-cancel",
#                 kwargs={"borrowing_id": borrowing.id}
#             )
#         )
#     )
#     return session
