# Generated by Django 4.0.4 on 2023-04-01 15:35

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_post_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reportpdf',
            field=models.FileField(default=False, storage=post.models.OverwriteStorage, upload_to='report/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default=False, upload_to='img/%m-%y'),
        ),
    ]