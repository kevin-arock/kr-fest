# Generated by Django 4.0.4 on 2023-03-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_dept_post_etype'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pay',
            field=models.IntegerField(null=True),
        ),
    ]