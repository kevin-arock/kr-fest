# Generated by Django 4.0.4 on 2023-03-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_approvedpost_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApprovedPost',
        ),
        migrations.AddField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
        migrations.AddField(
            model_name='post',
            name='cllg',
            field=models.CharField(default=False, max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='venue',
            field=models.CharField(default=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='img/krce/%m-%y'),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]