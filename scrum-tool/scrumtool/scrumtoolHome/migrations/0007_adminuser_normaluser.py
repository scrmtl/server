# Generated by Django 3.0.3 on 2020-03-03 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumtoolHome', '0006_auto_20200303_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='normalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
