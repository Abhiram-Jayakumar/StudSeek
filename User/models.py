from django.db import models

from Admin.models import District, Place

# Create your models here.

class Providers(models.Model):
    ROLE_CHOICES = [
        ('bus_service', 'Bus Service Provider'),
        ('food_vendor', 'Food Vendor'),
        ('hostel', 'Hostel'),
        ('college', 'College'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)



class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)


class College(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    loc = models.URLField(blank=True, null=True)
    registered_by = models.ForeignKey(Providers, on_delete=models.CASCADE)

class FoodVendor(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    loc = models.URLField(blank=True, null=True) 
    registered_by = models.ForeignKey(Providers, on_delete=models.CASCADE)

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    loc = models.URLField(blank=True, null=True)
    registered_by = models.ForeignKey(Providers, on_delete=models.CASCADE)


class BusProvider(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    route_details = models.TextField()  
    registered_by = models.ForeignKey(Providers, on_delete=models.SET_NULL, null=True, blank=True)


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    Rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=0)
    description = models.TextField(blank=True, null=True)


class BookingRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  
    capacity = models.PositiveIntegerField() 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    booking_date = models.DateTimeField(auto_now_add=True)  
    booking_status = models.CharField(max_length=20, choices=[  
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    rental_service_approval_status = models.BooleanField(default=False)  
    check_in_date = models.DateTimeField(null=True, blank=True)  
    special_requests = models.TextField(null=True, blank=True)
    payment = models.BooleanField(default=False)  
