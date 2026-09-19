"""
views.py — Heavy Machinery Rental Management System
"""
from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Machinery, Customer, Booking, Payment
from .serializers import (
    CategorySerializer, MachinerySerializer, CustomerSerializer,
    BookingSerializer, PaymentSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Public read access for GET/HEAD/OPTIONS; write access restricted to staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]


class MachineryViewSet(viewsets.ModelViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(customer__user=self.request.user)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'Approved'
        booking.save()
        return Response({'status': 'booking confirmed'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()
        return Response({'status': 'booking rejected'})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class DashboardViewSet(viewsets.ViewSet):
    """
    Admin dashboard: revenue and overdue reports.
    Mount at /api/dashboard/ in urls.py.
    """
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        total = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        return Response({'total_revenue': total})

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        today = timezone.now().date()
        overdue_bookings = Booking.objects.filter(
            end_date__lt=today,
            status='confirmed',
        )
        serializer = BookingSerializer(overdue_bookings, many=True)
        return Response(serializer.data)