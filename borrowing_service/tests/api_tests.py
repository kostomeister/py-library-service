import os

import stripe
from django.utils import timezone

from django.urls import reverse
from django.test import TestCase
from dotenv import load_dotenv
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from borrowing_service.models import Borrowing
from book_service.models import Book
from borrowing_service.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)

load_dotenv()

BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            "test1@user.com", "testpassword"
        )
        self.user2 = get_user_model().objects.create_user(
            "test2@user.com", "testpassword"
        )
        self.client.force_authenticate(self.user1)
        self.book = Book.objects.create(
            title="testbook",
            author="testauthor",
            cover="HARD",
            inventory=3,
            daily_fee=10.03,
        )
        self.book2 = Book.objects.create(
            title="testbook",
            author="testauthor",
            cover="HARD",
            inventory=0,
            daily_fee=10.03,
        )
        self.borrowing1 = Borrowing.objects.create(
            borrow_date="2023-10-17",
            expected_return_date="2023-10-25",
            book_id=self.book,
            user_id=self.user1,
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date="2023-10-17",
            expected_return_date="2023-10-25",
            book_id=self.book,
            user_id=self.user2,
        )

    def test_list_borrowing(self):
        response = self.client.get(BORROWING_URL)
        serializer1 = BorrowingListSerializer(self.borrowing1)
        serializer2 = BorrowingListSerializer(self.borrowing2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_create_borrowing(self):
        payload = {
            "expected_return_date": timezone.now().date(),
            "book_id": self.book.id,
        }
        response = self.client.post(BORROWING_URL, payload)
        book = Book.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book.inventory, 2)
        self.assertEqual(response.data["user_id"], self.user1.id)

    def test_create_borrowing_with_invalid_date(self):
        payload = {
            "expected_return_date": "2001-06-08",
            "book_id": self.book.id,
        }
        response = self.client.post(BORROWING_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = "Expected return date cannot be in the past."
        self.assertEqual(expected_error_message, response.data["non_field_errors"][0])

    def test_create_borrowing_with_invalid_book_inventory(self):
        payload = {
            "expected_return_date": "2001-06-08",
            "book_id": self.book2.id,
        }
        response = self.client.post(BORROWING_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_message = "This book is not available for borrowing now"
        self.assertEqual(expected_error_message, response.data["non_field_errors"][0])

    def test_retrieve_borrowing(self):
        response = self.client.get(detail_url(self.borrowing1.id))
        serializer = BorrowingDetailSerializer(self.borrowing1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AdminBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            "test1@user.com", "testpassword", is_staff=True
        )
        self.user2 = get_user_model().objects.create_user(
            "test2@user.com", "testpassword"
        )
        self.client.force_authenticate(self.user1)
        self.book = Book.objects.create(
            title="testbook",
            author="testauthor",
            cover="HARD",
            inventory=3,
            daily_fee=10.03,
        )
        self.borrowing1 = Borrowing.objects.create(
            borrow_date="2023-10-17",
            expected_return_date="2023-12-25",
            book_id=self.book,
            user_id=self.user2,
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date="2023-10-17",
            expected_return_date="2023-10-25",
            actual_return="2023-10-26",
            book_id=self.book,
            user_id=self.user1,
        )

    def test_list_borrowing(self):
        response = self.client.get(BORROWING_URL)
        serializer = BorrowingListSerializer(self.borrowing1)

        self.assertIn(serializer.data, response.data)

    def test_filter_borrowing_by_user_id(self):
        response = self.client.get(BORROWING_URL, {"user_id": self.user2.id})
        serializer1 = BorrowingListSerializer(self.borrowing1)
        serializer2 = BorrowingListSerializer(self.borrowing2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_borrowing_by_is_active(self):
        response = self.client.get(BORROWING_URL, {"is_active": True})
        serializer1 = BorrowingListSerializer(self.borrowing1)
        serializer2 = BorrowingListSerializer(self.borrowing2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_return_book(self):
        stripe.api_key = os.environ.get("STRIPE_SECRET_API_KEY")

        inventory = self.book.inventory
        response = self.client.post(f"/api/borrowings/{self.borrowing1.id}/return/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.borrowing1.refresh_from_db()
        self.book.refresh_from_db()

        self.assertTrue(self.borrowing1.actual_return)
        self.assertEqual(self.book.inventory, inventory + 1)

    def test_return_already_returned_book(self):
        self.borrowing1.actual_return = timezone.now().date()
        self.borrowing1.save()
        response = self.client.post(f"/api/borrowings/{self.borrowing1.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"error": "You already have a link to pay the fine or have successfully "
                                     "returned the book"}
        )
