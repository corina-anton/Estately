from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here:

class Property(models.Model):

    CONTRACT_TYPE_CHOICES = [
        ('rent', 'To rent'),
        ('buy', 'To buy')
    ]

    PROP_TYPE_CHOICES = [
        ('house', 'house'),
        ('flat / apartment', 'flat / apartment'),
        ('bungalow', 'bungalow'),
        ('land', 'land'),
        ('commercial property', 'commercial property'),
        ('other', 'other')
    ]

    FURNISH_TYPE_CHOICES = [
        ('F', 'furnished'),
        ('UF', 'unfurnished'),
        ('PF', 'partially furnished')
    ]

    NO_BEDROOMS_CHOICES = [
        ('0', 'studio'),
        ('1', '1 bedroom'),
        ('2', '2 bedrooms'),
        ('3', '3 bedrooms'),
        ('4', '4 bedrooms'),
        ('5', '5 bedrooms')
    ]

    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    type = models.CharField(choices=PROP_TYPE_CHOICES, max_length=20)
    price = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    furnish_type = models.CharField(choices=FURNISH_TYPE_CHOICES, max_length=2)
    contract_type = models.CharField(choices=CONTRACT_TYPE_CHOICES, max_length=4)
    no_bedrooms = models.CharField(choices=NO_BEDROOMS_CHOICES, max_length=1)
    no_bathrooms = models.IntegerField(default=1, validators=[MaxValueValidator(15)])
    features = models.TextField(max_length=500)
    description = models.TextField(max_length=800)
    address = models.CharField(max_length=250)

    # Helper:
    def get_thumbnail(self):
        if self.photo_set.count():
            return self.photo_set.all()[0].photo
        else:
            return "static/hero_image.jpg"


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    postcode = models.CharField(max_length=15)
    email = models.EmailField(max_length=40, unique=True)
    password = models.TextField()

    # REQUIRED_FIELDS=[]
    # # This forces Django to use the email as the username. The username is
    # # used as part of the authentication checks performed by
    # # `authenticate()` function
    # USERNAME_FIELD='email'

class Photo(models.Model):
    property = models.ForeignKey(Property, on_delete = models.CASCADE, null = True)
    photo = models.ImageField(upload_to='media/')
