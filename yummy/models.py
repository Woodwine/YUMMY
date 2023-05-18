from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.files.storage import FileSystemStorage
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.urls import reverse
from transliterate import slugify

from user.models import Profile


class CuisineType(ChoiceEnum):
    russia = 'Русская кухня'
    france = 'Французская кухня'
    georgia = 'Грузинская кухня'
    italia = 'Итальянская кухня'
    japan = 'Японская кухня'
    india = 'Индийская кухня'
    china = 'Китайская кухня'
    asia = 'Азиатская кухня'
    mexico = 'Мексиканская кухня'
    europe = 'Европейская кухня'
    caucasus = 'Кавказская кухня'
    uzbekistan = 'Узбекская кухня'
    turkey = 'Турецкая кухня'
    america = 'Американская кухня'
    spain = 'Испанская кухня'
    greece = 'Греческая кухня'


class DepartmentType(ChoiceEnum):
    salads = 'Салаты'
    soups = 'Первые блюда'
    main_dishes = 'Вторые блюда'
    snacks = 'Закуски'
    bakery = 'Выпечка'
    desserts = 'Десерты'
    drinks = 'Напитки'
    sauces = 'Соусы'
    canned = 'Заготовки на зиму'


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
    M = 'Мясо и птица'
    F = 'Рыба'
    V = 'Овощи'
    EG = 'Яйца'
    FR = 'Ягоды и фрукты'
    P = 'Крупы и макароны'
    SP = 'Специи'
    SS = 'Соусы'
    ML = 'Молочные продукты'
    B = 'Мука и ингредиенты для выпечки'
    D = 'Напитки'
    N = 'Орехи и сухофрукты'


class Goods(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(3)],
                            error_messages={'unique': 'Продукт с таким названием уже существует'},
                            verbose_name='Название продукта')
    type = EnumChoiceField(GoodsType, default=GoodsType.V, verbose_name='Тип продукта')

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product-details', args=[self.id])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('type',)


class Recipe(models.Model):
    """A class for presenting a recipe"""

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)], verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', verbose_name='Фотография')
    slug = models.SlugField(null=False, unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time = models.PositiveIntegerField(default=0, verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Приготовление')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    ingredients = models.ManyToManyField(Goods, default='', through='Ingredient', through_fields=['recipe', 'ingredient'],
                                         verbose_name='Ингредиент')
    cuisine = EnumChoiceField(CuisineType, blank=True, verbose_name='Кухня')
    department = EnumChoiceField(DepartmentType, default=DepartmentType.soups, verbose_name='Тип блюда')
    liked_by = models.ManyToManyField(Profile, related_name='liked_recipes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe-details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('date', 'name')


class Ingredient(models.Model):
    """A class for presenting an ingredient"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='Ингредиент')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    quantity_type = EnumChoiceField(ProductQuantity, default=ProductQuantity.GR, verbose_name='Единицы измерения')

    def __str__(self):
        return self.ingredient

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('ingredient', )


class Comments(models.Model):
    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    rating = models.IntegerField(choices=RATING_CHOICES, default=0, blank=True, null=True)
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор комментария')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        unique_together = ('recipe', 'comment_author')


