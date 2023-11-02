# Generated by Django 3.2.18 on 2023-10-23 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('choiceid', models.AutoField(primary_key=True, serialize=False)),
                ('choicetext', models.TextField()),
            ],
            options={
                'db_table': 'choice',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionid', models.AutoField(primary_key=True, serialize=False)),
                ('questiontext', models.TextField()),
                ('questiontype', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('surveyid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'survey',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('responseid', models.AutoField(primary_key=True, serialize=False)),
                ('respondentname', models.CharField(blank=True, max_length=255, null=True)),
                ('respondentemail', models.CharField(blank=True, max_length=255, null=True)),
                ('responsetext', models.TextField(blank=True, null=True)),
                ('responsenumeric', models.IntegerField(blank=True, null=True)),
                ('choiceid', models.ForeignKey(blank=True, db_column='choiceid', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGCISL.choice')),
                ('questionid', models.ForeignKey(blank=True, db_column='questionid', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGCISL.question')),
                ('surveyid', models.ForeignKey(blank=True, db_column='surveyid', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGCISL.survey')),
            ],
            options={
                'db_table': 'response',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='surveyid',
            field=models.ForeignKey(blank=True, db_column='surveyid', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGCISL.survey'),
        ),
        migrations.AddField(
            model_name='choice',
            name='questionid',
            field=models.ForeignKey(blank=True, db_column='questionid', null=True, on_delete=django.db.models.deletion.CASCADE, to='appGCISL.question'),
        ),
        migrations.CreateModel(
            name='GCISLUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('first_name', models.CharField(max_length=30, verbose_name='first')),
                ('last_name', models.CharField(max_length=30, verbose_name='last')),
                ('age_range', models.CharField(choices=[('1', '55-65'), ('2', '66-75'), ('3', '75+')], max_length=10, verbose_name='age')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('image', models.ImageField(default='/static/assets/general/icon.png', upload_to='static/assets/general/')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_resident', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
