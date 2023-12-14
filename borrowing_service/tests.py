from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from borrowing_service.models import Borrowing
from book_service.models import Book
from borrowing_service.serializers import BorrowingListSerializer

BORROWING_URL = reverse("borrowings:borrowing-list")


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
            expected_return_date="2023-10-25",
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
