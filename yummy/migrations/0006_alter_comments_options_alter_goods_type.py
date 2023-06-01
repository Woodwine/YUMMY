# Generated by Django 4.0.6 on 2023-05-24 18:18

from django.db import migrations
import enumchoicefield.fields
import yummy.models


class Migration(migrations.Migration):

    dependencies = [
        ('yummy', '0005_alter_comments_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='goods',
            name='type',
            field=enumchoicefield.fields.EnumChoiceField(default=yummy.models.GoodsType(6), enum_class=yummy.models.GoodsType, max_length=2, verbose_name='Тип продукта'),
        ),
    ]
