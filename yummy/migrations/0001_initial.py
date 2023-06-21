# Generated by Django 4.2.2 on 2023-06-20 11:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0006_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Продукт с таким названием уже существует.'}, max_length=50, unique=True, verbose_name='Название продукта')),
                ('type', models.CharField(choices=[('P', 'Крупы и макароны'), ('ML', 'Молочные продукты'), ('B', 'Мука и ингредиенты для выпечки'), ('M', 'Мясо и птица'), ('D', 'Напитки'), ('V', 'Овощи'), ('N', 'Орехи и сухофрукты'), ('F', 'Рыба'), ('SS', 'Соусы'), ('SP', 'Специи'), ('FR', 'Ягоды и фрукты'), ('EG', 'Яйца')], default='P', verbose_name='Тип продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(limit_value=1000, message='Количество слишком большое'), django.core.validators.MinValueValidator(limit_value=0.01, message='Количество слишком маленькое')], verbose_name='Количество')),
                ('quantity_type', models.CharField(choices=[('KG', 'кг.'), ('GR', 'гр.'), ('L', 'л.'), ('ML', 'мл.'), ('TEA_S', 'ч. л.'), ('TBL_S', 'ст. л.'), ('PC', 'шт.'), ('TST', 'по вкусу'), ('BN', 'банк.'), ('UP', 'уп.')], default='GR', verbose_name='Единицы измерения')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yummy.goods', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('ingredient__name', 'recipe__name'),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/', validators=[django.core.validators.validate_image_file_extension], verbose_name='Фотография готового блюда')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('time', models.PositiveIntegerField(default=0, verbose_name='Время приготовления')),
                ('description', models.TextField(max_length=4000, verbose_name='Приготовление')),
                ('cuisine', models.CharField(blank=True, choices=[('russia', 'Русская кухня'), ('france', 'Французская кухня'), ('georgia', 'Грузинская кухня'), ('italia', 'Итальянская кухня'), ('japan', 'Японская кухня'), ('india', 'Индийская кухня'), ('china', 'Китайская кухня'), ('asia', 'Азиатская кухня'), ('mexico', 'Мексиканская кухня'), ('europe', 'Европейская кухня'), ('caucasus', 'Кавказская кухня'), ('uzbekistan', 'Узбекская кухня'), ('turkey', 'Турецкая кухня'), ('america', 'Американская кухня'), ('spain', 'Испанская кухня'), ('greece', 'Греческая кухня')], verbose_name='Кухня')),
                ('department', models.CharField(choices=[('salads', 'Салаты'), ('soups', 'Первые блюда'), ('main_dishes', 'Вторые блюда'), ('snacks', 'Закуски'), ('bakery', 'Выпечка'), ('desserts', 'Десерты'), ('drinks', 'Напитки'), ('sauces', 'Соусы'), ('canned', 'Заготовки на зиму')], default='soups', verbose_name='Тип блюда')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.profile', verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(through='yummy.Ingredient', to='yummy.goods', verbose_name='Ингредиент')),
                ('liked_by', models.ManyToManyField(related_name='liked_recipes', to='user.profile', verbose_name='Пользователи, сохранившие рецепт')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-date', 'name'),
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yummy.recipe', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0, null=True)),
                ('comment', models.TextField(max_length=500, verbose_name='Комментарий')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile', verbose_name='Автор комментария')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yummy.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-date',),
                'unique_together': {('recipe', 'comment_author')},
            },
        ),
    ]
