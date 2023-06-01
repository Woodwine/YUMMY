# Generated by Django 4.0.6 on 2023-05-28 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_profile_options'),
        ('yummy', '0016_alter_comments_comment_alter_goods_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(max_length=500, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(error_messages={'unique': 'Продукт с таким названием уже существует.'}, max_length=50, unique=True, verbose_name='Название продукта'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(max_length=3000, verbose_name='Приготовление'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/', verbose_name='Фотография готового блюда'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_recipes', to='user.profile', verbose_name='Пользователи, сохранившие рецепт'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
    ]
