# Generated by Django 4.0.4 on 2023-03-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_approvedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedpost',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
