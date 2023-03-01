from django.db import models
from django.core.validators import MinLengthValidator
from user.models import User
from enumchoicefield import ChoiceEnum, EnumChoiceField
from enum import Enum
from django.urls import reverse

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
                            error_messages={'unique': 'Продукт с таким названием уже существует'})
    type = EnumChoiceField(GoodsType, default=GoodsType.V)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product-details', args=[self.id])


class Ingredient(models.Model):
    """A class for presenting an ingredient"""

    # INGREDIENTS = (
    #     ('мясо и птица', (
    #         ('chicken', 'курица'), ('beef', 'говядина'), ('pork', 'свинина'),
    #     )
    #      ),
    #     ('рыба', (
    #         ('salmon', 'лосось'), ('с_tuna', 'тунец консервированный'), ('mackerel', 'скумбрия'),
    #         ('pollock', 'минтай'), ('cod', 'треска'),
    #     )),
    #     ('овощи', (
    #         ('potato', 'картофель'), ('carrot', 'моковь'), ('onion', 'лук'), ('corn', 'кукуруза'),
    #         ('mushrooms', 'грибы'), ('lettuce', 'салат'), ('c_corn', 'консервированная кукуруза'),
    #         ('champignons', 'шампиньоны'), ('arugula', 'руккола'), ('cabbage', 'капуста'),
    #         ('cauliflower', 'цветная капуста'), ('broccoli', 'брокколи'), ('beet', 'свекла'),
    #         ('garlic', 'чеснок'), ('basil', 'базилик'), ('tomatoes', 'помидор'),
    #         ('cucumber', 'огурец'), ('paprika', 'сладкий перец'), ('hot_pepper', 'острый перец'),
    #         ('zucchini', 'кабачок'), ('eggplant', 'баклажан'), ('pumpkin', 'тыква'),
    #         ('b_olives', 'маслины'), ('olives', 'оливки'), ('string beans', 'стручковая фасоль'),
    #         ('parsley', 'петрушка'), ('cilantro', 'кинза'), ('dill', 'укроп'),
    #     )),
    #     ('яйца', (
    #         ('egg', 'яйцо'), ('yolk', 'желток'), ('protein', 'белок')
    #     )),
    #     ('фрукты', (
    #         ('apple', ''), ('orange', ''), ('banana', ''), ('strawberry', 'клубника'), ('peach', 'персик'),
    #         ('pear', 'груша'), ('grape', 'виноград'),
    #     )),
    #     ('крупы', (
    #         ('buckwheat', 'гречка'), ('haricot', 'фасоль'), ('lentils', 'чечевица'), ('rice', 'рис'),
    #         ('couscous', 'кускус'), ('bulgur', 'булгур'), ('pasta', 'макароны'), ('spaghetti', 'спагетти'),
    #     )),
    #     ('специи', (
    #         ('bl_pepper', 'черный перец'), ('cinnamon', 'корица'), ('coriander', 'кориандр'),
    #         ('mustard', 'горчица'), ('ginger', 'имбирь'), ('red wine', 'красное вино'),
    #         ('white wine', 'белое вино'), ('beer', 'пиво'),
    #     )),
    #     ('соусы', (
    #         ('mustard', 'горчица'), ('ketchup', 'кетчуп'), ('tomato paste', 'томатная паста'),
    #         ('mayonnaise', 'майонез'), ('balsamic', 'бальзамический соус'), ('vinegar', 'уксус'),
    #         ('lemon juice', 'лимонный сок'), ('sugar', 'сахар'), ('salt', 'соль'),
    #     )),
    #     ('молочные продукты', (
    #         ('milk', 'молоко'), ('sour cream', 'сметана'), ('cream', 'сливки'), ('kefir', 'кефир'),
    #         ('yogurt', 'йогурт'), ('curd', 'творог'), ('cheese', 'сыр'), ('parmesan', 'пармезан'),
    #         ('mozzarella', 'моцарелла')
    #     )),
    #     ('выпечка', (
    #         ('flour', 'мука'), ('yeasts', 'дрожжи'), ('soda', 'сода'), ('baking powder', 'разрыхлитель'),
    #
    #     )),
    #     ('напитки', (
    #         ('cocoa', 'какао'), ('coffee', 'кофе'), ('water', 'вода'), ('tea', 'чай'), ('apple juice', 'яблочный сок'),
    #         ('orange juice', 'апельсиновый сок'),
    #     )),
    #     ('сухофрукты', (
    #         ('raisin', 'изюм'), ('prunes', 'чернослив'), ('walnuts', 'грецкие орехи'),
    #         ('almond', 'миндаль'), ('peanut', 'арахис'), ('dried apricots', 'курага'),
    # )))

    ingredient = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    quantity_type = EnumChoiceField(ProductQuantity, default=ProductQuantity.GR, verbose_name='Колличество')

    def __str__(self):
        return self.ingredient


class Recipe(models.Model):
    """A class for presenting a recipe"""
    TIME = (
        ('min', ' мин'),
        ('hr', 'ч'),
    )

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)], verbose_name='Название')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL', null=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_in_minutes = models.PositiveIntegerField(verbose_name='Время приготовления', choices=TIME)
    description = models.TextField(verbose_name='Приготовление')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ингредиент', related_name='recipes')
    cuisine = EnumChoiceField(CuisineType, default=CuisineType.EUR, blank=True)
    department = EnumChoiceField(DepartmentType, default=DepartmentType.M)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('recipe-details', args=[self.slug])
