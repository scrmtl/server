# Generated by Django 3.0.3 on 2020-10-05 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_historicalepic_historicalfeature_historicaltask'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_template',
            field=models.BooleanField(default=False),
        ),
    ]