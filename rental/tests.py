from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta

from .models import Category, Customer, Machinery, Booking, Payment

class RentalAPITestCase(APITestCase):

    def setUp(self):
        # Create Users
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass123')
        self.regular_user = User.objects.create_user('john_doe', 'john@test.com', 'userpass123')

        # Create Category & Machinery
        self.category = Category.objects.create(name='Bulldozers', description='Heavy pushing equipment')
        self.machine = Machinery.objects.create(
            category=self.category,
            name='Caterpillar D6',
            rate_hourly=150.00,
            rate_daily=1000.00,
            status='Available'
        )

        # Create Customer
        self.customer = Customer.objects.create(
            name='John Doe',
            email='john@test.com',
            phone='1234567890',
            address='123 Main St',
            cnic='12345-6789012-3',
            password='userpass123'
        )

        # Create Booking
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(days=2)
        self.booking = Booking.objects.create(
            cust=self.customer,
            machine=self.machine,
            start_datetime=start,
            end_datetime=end,
            status='Pending',
            total_cost=2000.00
        )

    def test_get_machinery_list_public(self):
        """Anyone should be able to view machinery list."""
        response = self.client.get('/api/machinery/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_approve_booking_admin(self):
        """Admins can approve bookings via custom endpoint action."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/bookings/{self.booking.booking_id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'Approved')

    def test_approve_booking_unauthorized(self):
        """Unauthenticated or regular users cannot approve bookings."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(f'/api/bookings/{self.booking.booking_id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dashboard_stats_admin_only(self):
        """Dashboard endpoint is strictly accessible by staff/admins."""
        self.client.force_authenticate(user=self.regular_user)
        res_user = self.client.get('/api/dashboard/revenue/')
        self.assertEqual(res_user.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        res_admin = self.client.get('/api/dashboard/revenue/')
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
        self.assertIn('total_revenue', res_admin.data)