# Generated by Django 4.0.4 on 2023-03-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(blank=True, null=True, unique=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='pics/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]