from django.contrib import admin
from .models import Category, Customer, Machinery, Booking, Payment


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Machinery)
admin.site.register(Booking)
admin.site.register(Payment)