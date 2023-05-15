# Generated by Django 4.0.6 on 2023-05-12 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yummy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ('type',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('ingredient',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('date', 'name'), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yummy.goods', verbose_name='Ингредиент'),
        ),
    ]
