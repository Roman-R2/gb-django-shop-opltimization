# Generated by Django 3.2.9 on 2021-12-30 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_shopuserprofile_vk_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuserprofile',
            name='vk_avatar',
        ),
    ]