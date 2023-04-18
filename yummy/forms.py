from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Goods, Recipe, Ingredient


class AddProduct(forms.ModelForm):
    class Meta:
        model = Goods
        fields = '__all__'
        labels = {
            'name': 'Название продукта',
            'type': 'Тип продукта'
        }
        error_messages = {
            'name': {'max_length': 'Максимальное количество символов - 50',
                     'min_length': 'Минимальное количество символов - 3',
                     'required': 'Поле не может быть пустым'},
            'type': {'max_length': 'Максимальное количество символов - 50',
                     'min_length': 'Минимальное количество символов - 3',
                     'required': 'Поле не может быть пустым'},
        }


class AddIngredient(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient', 'quantity', 'quantity_type']
        labels = {
            'ingredient': 'Ингредиент',
            'quantity': 'Количество',
            'quantity_type': 'Единицы измерения',
        }
        error_messages = {
            'ingredient': {'required': 'Поле не может быть пустым'},
            'quantity': {'required': 'Поле не может быть пустым'},
            'quantity_type': {'required': 'Поле не может быть пустым'},
        }


class AddRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cuisine', 'department']
        labels = {
            'name': 'Название рецепта',
            'description': 'Приготовление',
            'cuisine': 'Кухня',
            'department': 'Тип блюда',
        }
        error_messages = {
            'name': {'max_length': 'Максимальное количество символов - 50',
                     'min_length': 'Минимальное количество символов - 3',
                     'required': 'Поле не может быть пустым'},
            'description': {'required': 'Поле не может быть пустым'},
            'department': {'required': 'Поле не может быть пустым'},
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 25}),
        }
