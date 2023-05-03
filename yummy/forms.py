from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms import inlineformset_factory
from .models import Goods, Recipe, Ingredient, GoodsType, CuisineType, DepartmentType, ProductQuantity


class RecipeImageInput(forms.ClearableFileInput):
    clear_checkbox_label = 'Удалить'
    input_text = 'Загрузить новый файл'
    template_name = "form_widgets/recipe_image_input.html"


class AddProduct(forms.ModelForm):
    class Meta:
        model = Goods
        fields = '__all__'
        labels = {
            'name': 'Название продукта',
            'type': 'Тип продукта'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название продукта'
            }),
            'type': forms.Select(choices=((i, GoodsType[i]) for i in GoodsType._member_names_), attrs={
                'class': 'form-select',
                'id': 'exampleSelect1',
            })
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


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=AddIngredient,
                                          fields=('ingredient', 'quantity', 'quantity_type'), extra=1,
                                          validate_max=False, can_delete=True, can_delete_extra=True,
                                          widgets={
                                              'ingredient': forms.Select(choices=Goods.objects.all(),
                                                                         attrs={
                                                                             'class': 'form-select'
                                                                         }),
                                              'quantity': forms.NumberInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Введите количество'}),
                                              'quantity_type': forms.Select(
                                                  choices=((i, ProductQuantity[i]) for i in
                                                           ProductQuantity._member_names_),
                                                  attrs={'class': 'form-select',
                                                         'id': 'exampleSelect4'})
                                          })


class AddRecipe(forms.ModelForm):
    time_in_hours = forms.IntegerField(required=False, label='Время приготовления (часов)',
                                       widget=forms.NumberInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Время (часов)'
                                       }))
    time_in_minutes = forms.IntegerField(required=True, error_messages={
                                                        'required': 'Поле не может быть пустым'},
                                         label='Время приготовления (минут)',
                                         widget=forms.NumberInput(attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Время (минут)'
                                         }))

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'cuisine', 'department']
        labels = {
            'name': 'Название рецепта',
            'image': 'Фотография блюда',
            'description': 'Приготовление',
            'cuisine': 'Кухня',
            'department': 'Тип блюда',
        }
        error_messages = {
            'name': {'max_length': 'Максимальное количество символов - 50',
                     'min_length': 'Минимальное количество символов - 3',
                     'required': 'Поле не может быть пустым'},
            'image': {'required': 'Поле не может быть пустым'},
            'description': {'required': 'Поле не может быть пустым'},
            'department': {'required': 'Поле не может быть пустым'},
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название рецепта'
            }),
            'image': RecipeImageInput(attrs={
                'class': 'form-control',
                'type': "file",
                'id': 'formFile',
                'placeholder': 'Выберите файл'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 50,
                'rows': 5,
                'placeholder': 'Приготовление'}),
            'cuisine': forms.Select(choices=((i, CuisineType[i]) for i in CuisineType._member_names_),
                                    attrs={
                                        'class': 'form-select',
                                        'id': 'exampleSelect2',
                                    }),
            'department': forms.Select(choices=((i, DepartmentType[i]) for i in DepartmentType._member_names_),
                                       attrs={
                                           'class': 'form-select',
                                           'id': 'exampleSelect3',
                                       })
        }
