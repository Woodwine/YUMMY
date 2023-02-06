from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(3)])
    surname = models.CharField(max_length=40, validators=[MinLengthValidator(3)])
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} {self.surname}'

