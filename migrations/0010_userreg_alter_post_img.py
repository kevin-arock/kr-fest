# Generated by Django 4.0.4 on 2023-03-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_post_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.DateField(null=True)),
                ('cllgname', models.TimeField()),
                ('sors', models.CharField(max_length=100)),
                ('verify', models.ImageField(blank=True, null=True, upload_to='users/%m-%y')),
                ('event', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='img/%m-%y'),
        ),
    ]