# Generated by Django 4.0.6 on 2023-05-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='users/Default_User.svg', upload_to='users/', verbose_name='Фотография профиля'),
        ),
    ]