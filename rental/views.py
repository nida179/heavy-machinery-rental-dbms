from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Customer, Machinery, Booking, Payment
from .serializers import (
    CategorySerializer, 
    CustomerSerializer,
    MachinerySerializer, 
    BookingSerializer, 
    PaymentSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MachineryViewSet(viewsets.ModelViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name']

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'Approved'
        booking.save()
        return Response({'status': 'Booking approved successfully'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'Cancelled'
        booking.save()
        return Response({'status': 'Booking cancelled'})

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
        active_bookings = Booking.objects.filter(status='Approved').count()
        pending_bookings = Booking.objects.filter(status='Pending').count()
        total_machinery = Machinery.objects.count()

        return Response({
            'total_revenue': total_revenue,
            'active_bookings': active_bookings,
            'pending_bookings': pending_bookings,
            'total_machinery': total_machinery,
        })