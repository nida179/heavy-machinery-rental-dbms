"""
serializers.py — Heavy Machinery Rental Management System
Adjust field names below to match your actual models.py if they differ.
"""
from rest_framework import serializers
from .models import Category, Machinery, Customer, Booking, Payment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MachinerySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Machinery
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # remove this line if Customer has no password field
        }

class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='cust.name',
        read_only=True
    )

    machinery_name = serializers.CharField(
        source='machine.name',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('total_cost',)

    def validate(self, data):
        """
        Prevent overlapping bookings for the same machinery.
        """

        machine = data.get(
            'machine',
            getattr(self.instance, 'machine', None)
        )

        start_datetime = data.get(
            'start_datetime',
            getattr(self.instance, 'start_datetime', None)
        )

        end_datetime = data.get(
            'end_datetime',
            getattr(self.instance, 'end_datetime', None)
        )

        # Check dates
        if start_datetime and end_datetime:
            if start_datetime >= end_datetime:
                raise serializers.ValidationError(
                    "End date/time must be after start date/time."
                )

        # Check overlapping bookings
        if machine and start_datetime and end_datetime:

            conflicting = Booking.objects.filter(
                machine=machine,
                status__in=[
                    'Pending',
                    'Approved',
                    'Ongoing'
                ],
                start_datetime__lt=end_datetime,
                end_datetime__gt=start_datetime,
            )

            # When updating an existing booking,
            # don't compare it against itself.
            if self.instance:
                conflicting = conflicting.exclude(
                    pk=self.instance.pk
                )

            if conflicting.exists():
                raise serializers.ValidationError(
                    "This machinery is already booked "
                    "for the selected time period."
                )

        return data
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate_booking(self, value):
        """Enforce 1:1 — a booking can only have one payment."""
        if self.instance is None and Payment.objects.filter(booking=value).exists():
            raise serializers.ValidationError("A payment already exists for this booking.")
        return value