from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from book_service.models import Book
from borrowing_service.models import Borrowing
from payment_service.models import Payment


class PaymentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="testpass"
        )
        self.client.force_authenticate(self.user)

        self.book = Book.objects.create(
            title="Test Book", inventory=2, daily_fee=0.05
        )

        self.borrowing = Borrowing.objects.create(
            book_id=self.book,
            expected_return_date="2020-01-01",
            user_id=self.user,
        )

        self.payment = Payment.objects.create(
            borrowing=self.borrowing,
            status=Payment.StatusChoices.PENDING,
            money_to_pay=10,
            type=Payment.TypeChoices.PAYMENT,
            session_url="http://testurl.com",
            session_id=1,
        )

    def test_payment_list(self):
        response_get = self.client.get(reverse("payments:payment-list"))
        response_post = self.client.post(reverse("payments:payment-list"))

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(len(response_get.data), 1)
        self.assertEqual(
            response_get.data[0]["borrowing"], self.payment.borrowing.id
        )

    def test_success_view(self):
        response = self.client.get(
            reverse(
                "payments:payment-success",
                args=[self.payment.borrowing_id]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.StatusChoices.PAID)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 1)

    def test_success_fine_view(self):
        borrowing = Borrowing.objects.create(
            book_id=self.book,
            expected_return_date="2021-01-01",
            user_id=self.user,
        )

        payment = Payment.objects.create(
            borrowing=borrowing,
            status=Payment.StatusChoices.PENDING,
            money_to_pay=10,
            type=Payment.TypeChoices.FINE,
            session_url="http://sessionurl.com",
            session_id=1,
        )

        response = self.client.get(
            reverse(
                "payments:payment-success-fine",
                args=[payment.borrowing_id]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.StatusChoices.PAID)
        self.assertEqual(payment.type, Payment.TypeChoices.PAYMENT)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 3)

    def test_cancel_view(self):
        response = self.client.get(
            reverse(
                "payments:payment-cancel",
                args=[self.payment.borrowing_id]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.StatusChoices.PENDING)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 2)
