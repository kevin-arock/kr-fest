# Generated by Django 4.1.7 on 2023-03-25 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_post_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default=True, max_length=300),
        ),
    ]
