# Generated by Django 4.0.4 on 2023-04-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_mode_remove_post_darkmode_remove_post_lightmode'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='report',
            field=models.BooleanField(default=False, verbose_name='report'),
        ),
    ]
