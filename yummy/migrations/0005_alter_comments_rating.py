# Generated by Django 4.0.6 on 2023-05-24 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yummy', '0004_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0, null=True),
        ),
    ]