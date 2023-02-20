from django.db import models
from django.core.validators import MinLengthValidator
from user.models import User

# Create your models here.


class Cuisine(models.Model):
    """A class to add a cuisine of a dish"""
    CUISINES = (
        ('ru', 'русская кухня'),
        ('fr', 'французская кухня'),
        ('gr', 'грузинская кухня'),
        ('it', 'итальянская кухня'),
        ('jp', 'японская кухня'),
        ('ind', 'индийская кухня'),
        ('chn', 'китайская кухня'),
        ('as', 'азиатская кухня'),
        ('mx', 'мексиканская кухня'),
        ('eur', 'европейская кухня'),
        ('kvz', 'кавказская кухня'),
        ('uz', 'узбекская кухня'),
        ('tr', 'турецкая кухня'),
        ('amr', 'американская кухня'),
        ('sp', 'испанская кухня'),
        ('ukr', 'украинская кухня'),
        ('grec', 'греческая кухня'),
        ('o', 'другие кухни')
    )

    cuisine_name = models.CharField(max_length=50, choices=CUISINES, blank=True)

    def __str__(self):
        return self.cuisine_name


class Department(models.Model):
    """A class for presenting a recipe department"""
    DEPARTMENTS = (
        ('b', 'выпечка'),
        ('d', 'дессерты'),
        ('m', 'вторые блюда'),
        ('s', 'закуски'),
        ('sal', 'салаты'),
        ('sp', 'первые блюда'),
        ('dr', 'напитки'),
        ('ss', 'соусы'),
        ('can', 'заготовки на зиму')
    )

    department_name = models.CharField(max_length=50, choices=DEPARTMENTS)

    def __str__(self):
        return self.department_name


class Ingredient(models.Model):
    """A class for presenting an ingredient"""
    PRODUCT_QUANTITY = (
        ('kg', 'кг'), ('gr', 'гр'),
        ('l', 'л'), ('ml', 'мл'),
        ('tea_s', 'ч. л.'), ('tbl_s', 'ст. л.'),
        ('tst', 'по вкусу'),
    )

    INGREDIENTS = (
        ('мясо и птица', (
            ('chicken', 'курица'), ('beef', 'говядина'), ('pork', 'свинина'),
        )
         ),
        ('рыба', (
            ('salmon', 'лосось'), ('с_tuna', 'тунец консервированный'), ('mackerel', 'скумбрия'),
            ('pollock', 'минтай'), ('cod', 'треска'),
        )),
        ('овощи', (
            ('potato', 'картофель'), ('carrot', 'моковь'), ('onion', 'лук'), ('corn', 'кукуруза'),
            ('mushrooms', 'грибы'), ('lettuce', 'салат'), ('c_corn', 'консервированная кукуруза'),
            ('champignons', 'шампиньоны'), ('arugula', 'руккола'), ('cabbage', 'капуста'),
            ('cauliflower', 'цветная капуста'), ('broccoli', 'брокколи'), ('beet', 'свекла'),
            ('garlic', 'чеснок'), ('basil', 'базилик'), ('tomatoes', 'помидор'),
            ('cucumber', 'огурец'), ('paprika', 'сладкий перец'), ('hot_pepper', 'острый перец'),
            ('zucchini', 'кабачок'), ('eggplant', 'баклажан'), ('pumpkin', 'тыква'),
            ('b_olives', 'маслины'), ('olives', 'оливки'), ('string beans', 'стручковая фасоль'),
            ('parsley', 'петрушка'), ('cilantro', 'кинза'), ('dill', 'укроп'),
        )),
        ('яйца', (
            ('egg', 'яйцо'), ('yolk', 'желток'), ('protein', 'белок')
        )),
        ('фрукты', (
            ('apple', ''), ('orange', ''), ('banana', ''), ('strawberry', 'клубника'), ('peach', 'персик'),
            ('pear', 'груша'), ('grape', 'виноград'),
        )),
        ('крупы', (
            ('buckwheat', 'гречка'), ('haricot', 'фасоль'), ('lentils', 'чечевица'), ('rice', 'рис'),
            ('couscous', 'кускус'), ('bulgur', 'булгур'), ('pasta', 'макароны'), ('spaghetti', 'спагетти'),
        )),
        ('специи', (
            ('bl_pepper', 'черный перец'), ('cinnamon', 'корица'), ('coriander', 'кориандр'),
            ('mustard', 'горчица'), ('ginger', 'имбирь'), ('red wine', 'красное вино'),
            ('white wine', 'белое вино'), ('beer', 'пиво'),
        )),
        ('соусы', (
            ('mustard', 'горчица'), ('ketchup', 'кетчуп'), ('tomato paste', 'томатная паста'),
            ('mayonnaise', 'майонез'), ('balsamic', 'бальзамический соус'), ('vinegar', 'уксус'),
            ('lemon juice', 'лимонный сок'), ('sugar', 'сахар'), ('salt', 'соль'),
        )),
        ('молочные продукты', (
            ('milk', 'молоко'), ('sour cream', 'сметана'), ('cream', 'сливки'), ('kefir', 'кефир'),
            ('yogurt', 'йогурт'), ('curd', 'творог'), ('cheese', 'сыр'), ('parmesan', 'пармезан'),
            ('mozzarella', 'моцарелла')
        )),
        ('выпечка', (
            ('flour', 'мука'), ('yeasts', 'дрожжи'), ('soda', 'сода'), ('baking powder', 'разрыхлитель'),

        )),
        ('напитки', (
            ('cocoa', 'какао'), ('coffee', 'кофе'), ('water', 'вода'), ('tea', 'чай'), ('apple juice', 'яблочный сок'),
            ('orange juice', 'апельсиновый сок'),
        )),
        ('сухофрукты', (
            ('raisin', 'изюм'), ('prunes', 'чернослив'), ('walnuts', 'грецкие орехи'),
            ('almond', 'миндаль'), ('peanut', 'арахис'), ('dried apricots', 'курага'),
    )))

    ingredient = models.CharField(max_length=40, choices=INGREDIENTS)
    quantity = models.PositiveIntegerField(choices=PRODUCT_QUANTITY, verbose_name='Колличество')

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ингредиент', related_name='recipes')
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL, blank=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
