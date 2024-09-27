
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Login(AbstractUser):
    is_user=models.BooleanField(default=False)
    is_manager=models.BooleanField(default=False)
    email=models.EmailField()
    company_name=models.TextField(max_length=100)
    company_address=models.TextField(max_length=100)
    phone=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    address=models.TextField(max_length=100)
    is_blocked = models.BooleanField(default=False)

class HomeStayDestination(models.Model):
    image=models.TextField()
    destination_name=models.CharField(max_length=100)
class HotelDestination(models.Model):
    image=models.TextField()
    destination_name=models.CharField(max_length=100)



# homestay
class Homestays(models.Model):
    name = models.CharField(max_length=100)
    facilities = models.TextField()
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=100)
    details = models.TextField()
    address= models.CharField(max_length=255)
    city=models.CharField(max_length=255)
class HomestayImage(models.Model):
    homestay = models.ForeignKey(Homestays, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='homestay_images/')

class HomeStayReview(models.Model):
    homestays = models.ForeignKey('Homestays',related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100)

class HomestayBooking(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    homestay = models.ForeignKey(Homestays, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_rooms = models.IntegerField()
    room_type = models.CharField(max_length=255)
    total_price=models.CharField(max_length=255)


class HomestayPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    payment_id = models.CharField(max_length=255, unique=True)
    payer_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





#hotel
class Hotels(models.Model):
     name = models.CharField(max_length=255)
     description = models.TextField()
     address = models.CharField(max_length=255)
     city = models.CharField(max_length=100)
     state = models.CharField(max_length=100)
     details= models.TextField()
     phone_number = models.CharField(max_length=20)
     facilities = models.TextField()
     price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     average_rating = models.FloatField(default=0)
     number_of_reviews = models.IntegerField(default=0)

class HotelImage(models.Model):
    hotels=models.ForeignKey(Hotels,related_name='images',on_delete=models.CASCADE)
    images=models.ImageField(upload_to='hotel_images/')

class HotelReview(models.Model):
    hotel = models.ForeignKey('Hotels', related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)

class Bookings(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_rooms = models.IntegerField()
    room_type = models.CharField(max_length=255)
    total_price=models.CharField(max_length=255)
    # payment_status = models.CharField(max_length=20, default='Pending')
    # stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)


class HotelPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    payment_id = models.CharField(max_length=255, unique=True)
    payer_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)