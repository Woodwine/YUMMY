from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import GoodsType, CuisineType, DepartmentType, ProductQuantity, Goods


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