# Generated by Django 4.0.6 on 2023-05-24 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yummy', '0011_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('ingredient__name', 'recipe__name'), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
    ]
