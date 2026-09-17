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
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    machinery_name = serializers.CharField(source='machinery.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('total_amount',)  # remove if you don't auto-calculate this

    def validate(self, data):
        """
        Booking-conflict validation: prevent double-booking the same machinery
        for overlapping date ranges.
        """
        machinery = data.get('machinery') or getattr(self.instance, 'machinery', None)
        start_date = data.get('start_date') or getattr(self.instance, 'start_date', None)
        end_date = data.get('end_date') or getattr(self.instance, 'end_date', None)

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date must be before end_date.")

        if machinery and start_date and end_date:
            conflicting = Booking.objects.filter(
                machinery=machinery,
                status__in=['pending', 'confirmed'],  # adjust to match your status choices
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if self.instance:
                conflicting = conflicting.exclude(pk=self.instance.pk)

            if conflicting.exists():
                raise serializers.ValidationError(
                    "This machinery is already booked for an overlapping date range."
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