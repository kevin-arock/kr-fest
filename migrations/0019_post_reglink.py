# Generated by Django 4.0.4 on 2023-04-14 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0018_post_reportpdf_alter_post_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reglink',
            field=models.CharField(default=True, max_length=300),
        ),
    ]
