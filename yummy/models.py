from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, validate_image_file_extension
from django.urls import reverse
from transliterate import slugify

from user.models import Profile

RATING_CHOICES = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

GOODS_TYPE = [
    ('P', 'Крупы и макароны'),
    ('ML', 'Молочные продукты'),
    ('B', 'Мука и ингредиенты для выпечки'),
    ('M', 'Мясо и птица'),
    ('D', 'Напитки'),
    ('V', 'Овощи'),
    ('N', 'Орехи и сухофрукты'),
    ('F', 'Рыба'),
    ('SS', 'Соусы'),
    ('SP', 'Специи'),
    ('FR', 'Ягоды и фрукты'),
    ('EG', 'Яйца'),
]

CUISINE_TYPE = [
    ('russia', 'Русская кухня'),
    ('france', 'Французская кухня'),
    ('georgia', 'Грузинская кухня'),
    ('italia', 'Итальянская кухня'),
    ('japan', 'Японская кухня'),
    ('india', 'Индийская кухня'),
    ('china', 'Китайская кухня'),
    ('asia', 'Азиатская кухня'),
    ('mexico', 'Мексиканская кухня'),
    ('europe', 'Европейская кухня'),
    ('caucasus', 'Кавказская кухня'),
    ('uzbekistan', 'Узбекская кухня'),
    ('turkey', 'Турецкая кухня'),
    ('america', 'Американская кухня'),
    ('spain', 'Испанская кухня'),
    ('greece', 'Греческая кухня')
]

DEPARTMENT_TYPE = [
    ('salads', 'Салаты'),
    ('soups', 'Первые блюда'),
    ('main_dishes', 'Вторые блюда'),
    ('snacks', 'Закуски'),
    ('bakery', 'Выпечка'),
    ('desserts', 'Десерты'),
    ('drinks', 'Напитки'),
    ('sauces', 'Соусы'),
    ('canned', 'Заготовки на зиму'),
]

PRODUCT_QUANTITY = [
    ('KG', 'кг.'),
    ('GR', 'гр.'),
    ('L', 'л.'),
    ('ML', 'мл.'),
    ('TEA_S', 'ч. л.'),
    ('TBL_S', 'ст. л.'),
    ('PC', 'шт.'),
    ('TST', 'по вкусу'),
    ('BN', 'банк.'),
    ('UP', 'уп.'),
]


class Goods(models.Model):
    """Represents a product consisting name and product type"""

    name = models.CharField(max_length=50, unique=True, verbose_name='Название продукта',
                            error_messages={'unique': 'Продукт с таким названием уже существует.'})
    type = models.CharField(choices=GOODS_TYPE, default='P', verbose_name='Тип продукта')

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product-details', args=[self.pk])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)


class Recipe(models.Model):
    """
    Represents a recipe consisting recipe name, photo of dish, slug, date of creation,
    cooking time, description, recipe author, ingredients of dish, cuisine type, dish type
    and users, who liked this recipe
    """

    name = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', validators=[validate_image_file_extension],
                              verbose_name='Фотография готового блюда')
    slug = models.SlugField(max_length=150, null=False, unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time = models.PositiveIntegerField(default=0, verbose_name='Время приготовления')
    description = models.TextField(max_length=4000, verbose_name='Приготовление')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    ingredients = models.ManyToManyField(Goods, through='Ingredient', through_fields=['recipe', 'ingredient'],
                                         verbose_name='Ингредиент')
    cuisine = models.CharField(choices=CUISINE_TYPE, default='russia', verbose_name='Кухня')
    department = models.CharField(choices=DEPARTMENT_TYPE, default='soups', verbose_name='Тип блюда')
    liked_by = models.ManyToManyField(Profile, related_name='liked_recipes',
                                      verbose_name='Пользователи, сохранившие рецепт')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe-details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(f'{self.name}') + '-' + f'{self.pk}'
            self.slug = slug
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date', 'name')


class Ingredient(models.Model):
    """Represents a dish ingredient consisting of product, quantity and unit of measurement"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='Ингредиент')
    quantity = models.FloatField(default=1,
                                 validators=[MaxValueValidator(limit_value=1000,
                                                               message='Количество слишком большое'),
                                             MinValueValidator(limit_value=0.01,
                                                               message='Количество слишком маленькое')],
                                 verbose_name='Количество')
    quantity_type = models.CharField(choices=PRODUCT_QUANTITY, default='GR', verbose_name='Единицы измерения')

    def __str__(self):
        return self.ingredient.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Comments(models.Model):
    """
    Represents a user comment of the dish consisting of commented recipe,
    rating, comment author, text of comment, date of comment
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    rating = models.IntegerField(choices=RATING_CHOICES, default=0, blank=True, null=True)
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор комментария')
    comment = models.TextField(max_length=500, verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        unique_together = ('recipe', 'comment_author')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-date',)
