from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):

    ADMIN = 1
    SELLER = 2
    CUSTOMER = 3
    PL = "pl"
    PH = "ph"
    JP = "jp"
    EN = "en"
    RU = "ru"
    FR = "fr"
    CH = "ch"
    AN = "an"
    BR = "br"
    OTHER = "Other"

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    )
    COUNTRY_CHOICES = {

        (PL, 'Poland'),
        (PH, 'Philippines'),
        (JP, 'Japan'),
        (EN, 'England'),
        (RU, 'Russia'),
        (FR, ''),
        (CH, 'ch'),
        (AN, 'an'),
        (BR, 'vr'),
        (OTHER, 'OTHER'),

    }
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CUSTOMER)
    street = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=250, blank=True)
    zip_code = models.CharField(max_length=250, blank=True)
    objects = CustomUserManager()
    country = models.CharField(
        max_length=250, blank=True, default=PH, choices=COUNTRY_CHOICES)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
