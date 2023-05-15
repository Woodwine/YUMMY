# Generated by Django 4.0.6 on 2023-05-10 16:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields
import yummy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Продукт с таким названием уже существует'}, max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Название продукта')),
                ('type', enumchoicefield.fields.EnumChoiceField(default=yummy.models.GoodsType(3), enum_class=yummy.models.GoodsType, max_length=2, verbose_name='Тип продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('quantity_type', enumchoicefield.fields.EnumChoiceField(default=yummy.models.ProductQuantity(2), enum_class=yummy.models.ProductQuantity, max_length=5, verbose_name='Единицы измерения')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yummy.goods', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['ingredient'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Фотография')),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('time', models.PositiveIntegerField(default=0, verbose_name='Время приготовления')),
                ('description', models.TextField(verbose_name='Приготовление')),
                ('cuisine', enumchoicefield.fields.EnumChoiceField(blank=True, enum_class=yummy.models.CuisineType, max_length=10)),
                ('department', enumchoicefield.fields.EnumChoiceField(default=yummy.models.DepartmentType(2), enum_class=yummy.models.DepartmentType, max_length=11)),
                ('ingredients', models.ManyToManyField(default='', through='yummy.Ingredient', to='yummy.goods', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['date', 'name'],
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yummy.recipe'),
        ),
    ]
