# Generated by Django 4.1.7 on 2023-03-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GCISLUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('first_name', models.CharField(max_length=30, verbose_name='first')),
                ('last_name', models.CharField(max_length=30, verbose_name='last')),
                ('age_range', models.CharField(max_length=20, verbose_name='age')),
                ('location', models.CharField(max_length=250, verbose_name='location')),
                ('faculty', models.BooleanField(default=False)),
                ('resident', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
