# Generated by Django 4.2 on 2023-06-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0022_alter_post_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(default=False, max_length=254)),
                ('cllgname', models.CharField(max_length=300)),
                ('sors', models.CharField(max_length=100)),
                ('verify', models.ImageField(blank=True, null=True, upload_to='users/%m-%y')),
                ('event', models.CharField(default=False, max_length=300)),
                ('fromcllg', models.CharField(default=False, max_length=300)),
            ],
        ),
    ]
