from django.db import models
# Each class -> becomes a table
# Each attribute -> becomes a column
# Each instance -> becomes a row

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=225)
    cnic = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Machinery(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Maintenance'),
    ]

    machine_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column='category_id',
        related_name='machines'
    )
    name = models.CharField(max_length=100)
    rate_hourly = models.DecimalField(max_digits=10, decimal_places=2)
    rate_daily = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    class Meta:
        verbose_name_plural = 'Machinery'

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    # Refers to Customer model (Assumed defined elsewhere in your app)
    cust = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        db_column='cust_id',
        related_name='bookings'
    )
    machine = models.ForeignKey(
        Machinery,
        on_delete=models.CASCADE,
        db_column='machine_id',
        related_name='bookings'
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.machine.name}"

class Payment(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cash')
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking}"