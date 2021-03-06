# Generated by Django 3.0.3 on 2020-07-15 20:23

import api.models.model_interfaces
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(blank=True,
                                           help_text='Begin of the project', null=True)),
                ('end', models.DateField(blank=True,
                                         help_text='End of the project', null=True)),
                ('version', models.TextField(help_text='The Version of the product after the             sprint is finished (V00.00.00.00)',
                                             max_length=12, validators=[django.core.validators.RegexValidator('^ V\\d{1, 2}\\.\\d{1, 2}\\.\\d{1, 2}\\.\\d{1, 2}$')])),
                ('number', models.IntegerField(
                    help_text='Describes the order of the steps')),
                ('story', models.TextField(
                    help_text='Story of the po that he wants to do in the sprint')),
                ('status', models.CharField(choices=[('NW', 'new'), ('IL', 'planning'), ('PL', 'planned'), (
                    'IR', 'in_progress'), ('DO', 'done'), ('AC', 'accepted')], default='NW', max_length=2)),
                ('project', models.ForeignKey(help_text='Project this sprint object is part of.',
                                              on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='api.Project')),
            ],
            options={
                'verbose_name': 'Sprint',
                'verbose_name_plural': 'Sprints',
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model,
                   api.models.model_interfaces.IGetProject),
        ),
        migrations.AddField(
            model_name='epic',
            name='sprint',
            field=models.ForeignKey(blank=True, help_text='Sprint this card is part of.', null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='epic_cards', to='api.Sprint'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feature',
            name='sprint',
            field=models.ForeignKey(blank=True, help_text='Sprint this card is part of.', null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='feature_cards', to='api.Sprint'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(blank=True, help_text='Sprint this card is part of.', null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='task_cards', to='api.Sprint'),
            preserve_default=False,
        ),
    ]
