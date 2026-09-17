"""
urls.py — Heavy Machinery Rental Management System (rental app)
Include this in your project's main urls.py with: path('api/', include('rental.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, MachineryViewSet, CustomerViewSet,
    BookingViewSet, PaymentViewSet, DashboardViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'machinery', MachineryViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]