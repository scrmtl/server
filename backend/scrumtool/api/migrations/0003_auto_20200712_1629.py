# Generated by Django 3.0.3 on 2020-07-12 14:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200709_2340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrumuser',
            options={},
        ),
        migrations.RemoveField(
            model_name='lane',
            name='board',
        ),
        migrations.AddField(
            model_name='epic',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, help_text='User that are assigned to the card', related_name='epic_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feature',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, help_text='User that are assigned to the card', related_name='feature_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, help_text='User that are assigned to the card', related_name='task_cards', to=settings.AUTH_USER_MODEL),
        ),
    ]