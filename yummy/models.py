from django.db import models
from django.core.validators import MinLengthValidator
from user.models import User
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.urls import reverse
from transliterate import slugify


# Create your models here.


class CuisineType(ChoiceEnum):
    RU = 'русская кухня'
    FR = 'французская кухня'
    GR = 'грузинская кухня'
    IT = 'итальянская кухня'
    JP = 'японская кухня'
    IND = 'индийская кухня'
    CHN = 'китайская кухня'
    AS = 'азиатская кухня'
    MX = 'мексиканская кухня'
    EUR = 'европейская кухня'
    KVZ = 'кавказская кухня'
    UZ = 'узбекская кухня'
    TR = 'турецкая кухня'
    AMR = 'американская кухня'
    SP = 'испанская кухня'
    GRC = 'греческая кухня'


class DepartmentType(ChoiceEnum):
    B = 'выпечка'
    D = 'дессерты'
    M = 'вторые блюда'
    S = 'закуски'
    SL = 'салаты'
    SP = 'первые блюда'
    DR = 'напитки'
    SS = 'соусы'
    CAN = 'заготовки на зиму'


class ProductQuantity(ChoiceEnum):
    KG = 'кг.'
    GR = 'гр.'
    L = 'л.'
    ML = 'мл.'
    TEA_S = 'ч. л.'
    TBL_S = 'ст. л.'
    PC = 'шт.'
    TST = 'по вкусу'


class GoodsType(ChoiceEnum):
    M = 'мясо и птица'
    F = 'рыба'
    V = 'овощи'
    EG = 'яйца'
    FR = 'фрукты'
    P = 'крупы'
    SP = 'специи'
    SS = 'соусы'
    ML = 'молочные продукты'
    B = 'выпечка'
    D = 'напитки'
    N = 'сухофрукты'


class Goods(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(3)],
                            error_messages={'unique': 'Продукт с таким названием уже существует'}, verbose_name='Название продукта')
    type = EnumChoiceField(GoodsType, default=GoodsType.V, verbose_name='Тип продукта')

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product-details', args=[self.id])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['type']


class Recipe(models.Model):
    """A class for presenting a recipe"""

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)], verbose_name='Название')
    slug = models.SlugField(null=False, unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_in_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name='Время приготовления(ч.)')
    time_in_minutes = models.PositiveIntegerField(verbose_name='Время приготовления(мин.)')
    description = models.TextField(verbose_name='Приготовление')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    ingredients = models.ManyToManyField(Goods, through='Ingredient', through_fields=['recipe', 'ingredient'], verbose_name='Ингредиент', blank=True)
    cuisine = EnumChoiceField(CuisineType, default=CuisineType.EUR, blank=True)
    department = EnumChoiceField(DepartmentType, default=DepartmentType.M)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'recipes/{self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['date', 'name']


class Ingredient(models.Model):
    """A class for presenting an ingredient"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name='Количество')
    quantity_type = EnumChoiceField(ProductQuantity, default=ProductQuantity.GR, verbose_name='Единицы измерения')

    def __str__(self):
        return self.ingredient

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['ingredient']
