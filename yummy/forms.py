from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator, \
    validate_integer, validate_image_file_extension
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Goods, Recipe, Ingredient, GoodsType, CuisineType, DepartmentType, ProductQuantity, Comments


class RecipeImageInput(forms.ClearableFileInput):
    clear_checkbox_label = 'Удалить'
    input_text = 'Загрузить новый файл'
    template_name = "form_widgets/recipe_image_input.html"


class AddProduct(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False, label='Название продукта',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Введите название продукта'
                           }),
                           validators=[MinLengthValidator(limit_value=3,
                                                          message='Название продукта слишком короткое'),
                                       MaxLengthValidator(limit_value=100,
                                                          message='Название продукта слишком длинное'
                                                          )])

    class Meta:
        model = Goods
        fields = ('name', 'type')
        labels = {
            'type': 'Тип продукта'
        }
        widgets = {
            'type': forms.Select(choices=((i, GoodsType[i]) for i in GoodsType._member_names_),
                                 attrs={
                                     'class': 'form-select',
                                     'id': 'exampleSelect1',
                                 })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == '' or name is None:
            raise forms.ValidationError(_('Поле не может быть пустым'))
        if not name.isalpha():
            raise forms.ValidationError(_('Название продукта не должно содержать цифры'))
        return name.capitalize()


class AddIngredient(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('ingredient', 'quantity', 'quantity_type')
        labels = {
            'ingredient': 'Ингредиент',
            'quantity': 'Количество',
            'quantity_type': 'Единицы измерения',
        }
        widgets = {
            'ingredient': forms.Select(
                choices=Goods.objects.all(),
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Выберите ингредиент'
                }),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Введите количество'}),
            'quantity_type': forms.Select(
                choices=((i, ProductQuantity[i]) for i in ProductQuantity._member_names_),
                attrs={'class': 'form-select',
                       'id': 'exampleSelect4'})
        }
        error_messages = {
            'ingredient': {
                'required': 'Поле не может быть пустым'
            },
            'quantity': {
                'required': 'Поле не может быть пустым'
            }
        }


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=AddIngredient,
                                          fields=('ingredient', 'quantity', 'quantity_type'), extra=1,
                                          max_num=1, validate_max=False, can_delete=True, can_delete_extra=True,
                                          )


class AddRecipe(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Название рецепта', required=False,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Введите название рецепта'
                           }),
                           validators=[MinLengthValidator(limit_value=3,
                                                          message='Название рецепта слишком короткое.'),
                                       MaxLengthValidator(limit_value=150,
                                                          message='Название рецепта слишком длинное.'
                                                          )])
    description = forms.CharField(max_length=4000, required=False, label='Приготовление',
                                  widget=forms.Textarea(attrs={
                                      'class': 'form-control',
                                      'cols': 50,
                                      'rows': 5,
                                      'placeholder': 'Приготовление'}),
                                  validators=[MinLengthValidator(limit_value=30,
                                                                 message='Описание рецепта слишком короткое.'),
                                              MaxLengthValidator(limit_value=4000,
                                                                 message='Описание рецепта слишком длинное.'
                                                                 )])
    time_in_hours = forms.IntegerField(initial=0, required=False, label='Время приготовления (часов)',
                                       widget=forms.NumberInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Время (часов)'
                                       }))
    time_in_minutes = forms.IntegerField(initial=0, required=False,
                                         label='Время приготовления (минут)',
                                         widget=forms.NumberInput(attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Время (минут)'
                                         }))

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cuisine', 'department', 'description',)
        labels = {
            'image': 'Фотография блюда',
            'cuisine': 'Кухня',
            'department': 'Тип блюда',
        }
        widgets = {
            'image': RecipeImageInput(attrs={
                                 'class': 'form-control',
                                 'type': "file",
                                 'id': 'formFile',
                                 'placeholder': 'Выберите файл'
                             }),
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
        error_messages = {
            'image': {
                'required': 'Поле не может быть пустым'
            }
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == '' or name is None:
            raise forms.ValidationError(_('Поле не может быть пустым'))
        if name.replace(' ', '').isdigit():
            raise forms.ValidationError(_('Название рецепта не может состоять только из цифр'))
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description == '' or description is None:
            raise forms.ValidationError(_('Поле не может быть пустым'))
        if description.replace(' ', '').isdigit():
            raise forms.ValidationError(_('Описание рецепта не может состоять только из цифр'))
        return description

    def clean(self):
        cleaned_data = super(AddRecipe, self).clean()
        time_in_hours = int(cleaned_data.get('time_in_hours')) if cleaned_data.get('time_in_hours') else 0
        time_in_minutes = int(cleaned_data.get('time_in_minutes')) if cleaned_data.get('time_in_minutes') else 0
        time = time_in_hours * 60 + time_in_minutes
        if time > 0:
            cleaned_data['time'] = time
        else:
            msg = 'Введите время приготовления (часов либо минут)'
            self.add_error("time_in_hours", msg)
            self.add_error("time_in_minutes", msg)


class AddComment(forms.ModelForm):
    comment = forms.CharField(max_length=500, required=False, label='Комментарий',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Оставьте комментарий к рецепту'
                              }),
                              validators=[MinLengthValidator(limit_value=3,
                                                             message='Комментарий слишком короткий'),
                                          MaxLengthValidator(limit_value=500,
                                                             message='Комментарий слишком длинный')])

    class Meta:
        model = Comments
        fields = ['comment']

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment == '' or comment is None:
            raise forms.ValidationError(_('Поле не может быть пустым'))
        return comment
