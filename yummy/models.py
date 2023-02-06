from django.db import models
from django.core.validators import MinLengthValidator
from user.models import User

# Create your models here.


class Cuisine(models.Model):
    """A class to add a dish cuisine"""
    cuisine_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cuisine_name


class Department(models.Model):
    """A class for presenting a recipe department"""
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name


class Ingredient(models.Model):
    """A class for presenting an ingredient"""
    ingredient = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(verbose_name='Колличество')

    def __str__(self):
        return self.ingredient


class Recipe(models.Model):
    """A class for presenting a recipe"""
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)], verbose_name='Название')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_in_minutes = models.PositiveIntegerField(verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Приготовление')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ингредиент', related_name='recipes')
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
