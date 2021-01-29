from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from utils.models import CRideModel

class User(CRideModel, AbstractUser):
    
    email = models.EmailField(
        'email_address',
        unique=True,
        error_messages={
            'unique': 'ya existe un usuario con este mail'
        }
    )

    phone_regex = RegexValidator(
        regex = r'\+?1?\d{8,15}$',
        message='El telefono debe cumplir el formato +111111111'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    # por defeto todos los usuarios son clientes
    is_client = models.BooleanField(
        'client_status',
        default=True,
    )
    # indica si un usuario esta verificado o no
    is_verified = models.BooleanField(
        'verified', 
        default=False,
    )

    USERNAME_FIELD = 'email' #valor por defecto para login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name',] # campos obligatorios

    def __str__(self):
        return self.username

    def __get_short_name__(self):
        return self.username

    