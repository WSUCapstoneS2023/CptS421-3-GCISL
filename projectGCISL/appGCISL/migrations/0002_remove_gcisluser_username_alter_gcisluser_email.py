# Generated by Django 4.1.7 on 2023-04-18 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGCISL', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gcisluser',
            name='username',
        ),
        migrations.AlterField(
            model_name='gcisluser',
            name='email',
            field=models.EmailField(max_length=60, unique=True, verbose_name='email'),
        ),
    ]