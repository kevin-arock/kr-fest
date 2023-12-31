# Generated by Django 4.0.4 on 2023-03-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_alter_userreg_cllgname'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='darkmode',
            field=models.BooleanField(default=False, verbose_name='Dark'),
        ),
        migrations.AddField(
            model_name='post',
            name='lightmode',
            field=models.BooleanField(default=True, verbose_name='Light'),
        ),
    ]
