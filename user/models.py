from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='users/', default='users/user.svg', verbose_name='Фотография профиля')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('user__username', )


