# Generated by Django 4.2.4 on 2023-09-22 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGCISL', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('choiceid', models.IntegerField(primary_key=True, serialize=False)),
                ('choicetext', models.TextField()),
            ],
            options={
                'db_table': 'choice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionid', models.IntegerField(primary_key=True, serialize=False)),
                ('questiontext', models.TextField()),
                ('questiontype', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'question',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('responseid', models.IntegerField(primary_key=True, serialize=False)),
                ('respondentname', models.CharField(blank=True, max_length=255, null=True)),
                ('respondentemail', models.CharField(blank=True, max_length=255, null=True)),
                ('responsetext', models.TextField(blank=True, null=True)),
                ('responsenumeric', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'response',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('surveyid', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'survey',
                'managed': False,
            },
        ),
    ]