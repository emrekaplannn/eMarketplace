from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, DecimalField, URLField, IntField, BooleanField

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('vehicles', 'Vehicles'),
        ('computers', 'Computers'),
        ('phones', 'Phones'),
        ('private_lessons', 'Private Lessons'),
    ]
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png"
    image_url = models.URLField(blank=True, default=DEFAULT_IMAGE_URL)
    description = models.TextField()
    owner_id = models.IntegerField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        managed = True
        verbose_name = 'user'
        verbose_name_plural = 'users'

class FavoriteItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PriceHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_updated = models.DateTimeField(auto_now_add=True)


class Vehicle(Item):
    #item_id = models.IntegerField( default=None, blank=True, null=True)
    type = models.CharField(max_length=50, default=None, blank=True, null=True)
    brand = models.CharField(max_length=50, default=None, blank=True, null=True)
    model = models.CharField(max_length=50, default=None, blank=True, null=True)
    year = models.CharField(max_length=50, default=None, blank=True, null=True)
    color = models.CharField(max_length=50, default=None, blank=True, null=True)
    engine_displacement = models.CharField(max_length=50, default=None, blank=True, null=True)
    fuel_type = models.CharField(max_length=50, default=None, blank=True, null=True)
    transmission_type = models.CharField(max_length=50, default=None, blank=True, null=True)
    mileage = models.CharField(max_length=50, default=None, blank=True, null=True)
    #class Meta:
    #    verbose_name_plural = 'Vehicles'

class PrivateLesson(Item):
    item_id = models.IntegerField(null=True, default=None, blank=True)
    tutor_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    lessons = models.CharField(max_length=100, default=None, blank=True, null=True)
    location = models.CharField(max_length=100, default=None, blank=True, null=True)
    duration = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Private Lessons'

class Phone(Item):
    item_id = models.IntegerField( default=None, blank=True, null=True)
    brand = models.CharField(max_length=100, default=None, blank=True, null=True)
    model = models.CharField(max_length=100, default=None, blank=True, null=True)
    year = models.PositiveIntegerField( default=None, blank=True, null=True)
    operating_system = models.CharField(max_length=100, default=None, blank=True, null=True)
    processor = models.CharField(max_length=100, default=None, blank=True, null=True)
    ram = models.CharField(max_length=100, default=None, blank=True, null=True)
    storage = models.CharField(max_length=100, default=None, blank=True, null=True)
    camera_specifications = models.CharField(max_length=100, default=None, blank=True, null=True)
    battery_capacity = models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Phones'

class Computer(Item):
    item_id = models.IntegerField( default=None, blank=True, null=True)
    type = models.CharField(max_length=100, default=None, blank=True, null=True)
    brand = models.CharField(max_length=100, default=None, blank=True, null=True)
    model = models.CharField(max_length=100, default=None, blank=True, null=True)
    year = models.PositiveIntegerField( default=None, blank=True, null=True)
    processor = models.CharField(max_length=100, default=None, blank=True, null=True)
    ram = models.CharField(max_length=100, default=None, blank=True, null=True)
    storage = models.CharField(max_length=100, default=None, blank=True, null=True)
    graphics_card = models.CharField(max_length=100, default=None, blank=True, null=True)
    operating_system = models.CharField(max_length=100, default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Computers'


