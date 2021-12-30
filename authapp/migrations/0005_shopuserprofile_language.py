# Generated by Django 3.2.9 on 2021-12-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20211227_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='language',
            field=models.CharField(choices=[('Rus', 'Русский'), ('Eng', 'English'), ('Esp', 'Espaniol'), ('U', 'Неизвестно')], default='U', max_length=20, verbose_name='Язык'),
        ),
    ]