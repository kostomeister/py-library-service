from django.urls import path, include
from rest_framework import routers
from payment_service.views import (
    PaymentViewSet,
    SuccessView,
    CancelView, 
    SuccessFineView
)

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('<int:borrowing_id>/success/', SuccessView.as_view(), name='payment-success'),
    path('<int:borrowing_id>/success-fine/', SuccessFineView.as_view(), name='payment-success-fine'),
    path('<int:borrowing_id>/cancel/', CancelView.as_view(), name='payment-cancel'),
]

app_name = "payments"
