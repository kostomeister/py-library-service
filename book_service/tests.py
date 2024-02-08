from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


from book_service.models import Book
from book_service.serializers import (
    BookListSerializer,
    BookDetailSerializer,
)


def sample_book(**params):
    defaults = {
        "title": "SampleBook",
        "author": "SampleAuthor",
        "cover": "HARD",
        "inventory": 35,
        "daily_fee": 17.19,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


BOOK_URL = reverse("books:book-list")


def book_detail_url(book_id):
    return reverse("books:book-detail", args=[book_id])


class UnAuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = sample_book()
        self.book2 = sample_book(title="FilterBook")

    def test_filter_books_by_title(self):
        response = self.client.get(BOOK_URL, {"title": "filter"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer1 = BookListSerializer(self.book1)
        serializer2 = BookListSerializer(self.book2)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer1.data, response.data)

    def test_list_books(self):
        result = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_retrieve_book(self):
        url = book_detail_url(self.book1.id)
        response = self.client.get(url)
        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_unauthorized(self):
        payload = {
            "title": "SampleBook15",
            "author": "SampleAuthor15",
            "cover": "Hard",
            "inventory": 35,
            "daily_fee": 15.19,
        }
        result = self.client.post(BOOK_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_create_book_forbidden(self):
        payload = {
            "title": "SampleBook15",
            "author": "SampleAuthor15",
            "cover": "Hard",
            "inventory": 35,
            "daily_fee": 15.19,
        }
        result = self.client.post(BOOK_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        book = sample_book()
        url = book_detail_url(book.id)
        payload = {
            "title": "SampleBook15",
            "author": "SampleAuthor15",
            "cover": "Hard",
            "inventory": 35,
            "daily_fee": 15.19,
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book_forbidden(self):
        book = sample_book()
        url = book_detail_url(book.id)
        payload = {
            "inventory": 25,
            "daily_fee": 15.19,
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = sample_book()
        url = book_detail_url(book.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_update_book(self):
        book = sample_book()
        url = book_detail_url(book.id)
        payload = {
            "title": "SampleBook15",
            "author": "SampleAuthor15",
            "cover": "Hard",
            "inventory": 35,
            "daily_fee": 15.19,
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=response.data["id"])
        self.assertEqual(payload["daily_fee"], float(book.daily_fee))

        payload.pop("daily_fee")
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_create_book(self):
        payload = {
            "title": "SampleBook15",
            "author": "SampleAuthor15",
            "cover": "Hard",
            "inventory": 35,
            "daily_fee": 15.19,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=response.data["id"])
        self.assertEqual(payload["daily_fee"], float(book.daily_fee))

        payload.pop("daily_fee")
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_partial_update_book(self):
        book = sample_book()
        url = book_detail_url(book.id)
        payload = {
            "author": "SampleAuthor15",
            "inventory": 35,
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=response.data["id"])
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_delete_book(self):
        book = sample_book()
        url = book_detail_url(book.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)