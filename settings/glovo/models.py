from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('Client', 'Client'),
    ('Courier', 'Courier'),
    ('Seller', 'Seller')
)

CATEGORY_CHOICES = [
    ('Grocery', 'Grocery'),
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Beauty', 'Beauty'),
    ('Home', 'Home'),
    ('Sports', 'Sports'),
    ('Books', 'Books'),
    ('Toys', 'Toys'),
    ('Pharmacy', 'Pharmacy'),
    ('Automotive', 'Automotive'),
    ('Pet', 'Pet'),
    ('Other', 'Other'),
]

class User(AbstractUser):
    status = models.CharField(choices=STATUS_CHOICES, default='Client')
    data_registered = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.username

class Store(models.Model):
    store_image = models.ImageField(null=True, blank=True)
    store_name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES)
    item_1 = models.ImageField(upload_to='items/', null=True)
    item_2 = models.ImageField(upload_to='items/', null=True)
    item_3 = models.ImageField(upload_to='items/', null=True)
    item_4 = models.ImageField(upload_to='items/', null=True)
    item_5 = models.ImageField(upload_to='items/', null=True)
    item_6 = models.ImageField(upload_to='items/', null=True)
    item_7 = models.ImageField(upload_to='items/', null=True)
    item_8 = models.ImageField(upload_to='items/', null=True)
    item_9 = models.ImageField(upload_to='items/', null=True)
    item_10 = models.ImageField(upload_to='items/', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_phone_number = PhoneNumberField(region='KG')
    website = models.URLField()

    def __str__(self):
        return self.store_name

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.rate for r in ratings) / ratings.count(), 2)
        return None

class StoreRating(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='ratings')
    rate = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.store} - {self.rate}/5"

class Cart(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.TextField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.item

class Order(models.Model):
    your_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    contact_phone_number = PhoneNumberField(region='KG')

    def __str__(self):
        return self.address

class CourierRating(models.Model):
    courier = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.courier} - {self.rate}/5"