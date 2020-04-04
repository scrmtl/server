# Generated by Django 3.0.3 on 2020-03-30 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SprintBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('productBacklog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumtoolHome.ProductBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='Steplist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('storypoints', models.IntegerField(default=0)),
                ('label_frontend', models.BooleanField(default=False)),
                ('label_backend', models.BooleanField(default=False)),
                ('label_other', models.BooleanField(default=False)),
                ('sprintBacklog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumtoolHome.SprintBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='SteplistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('checked', models.BooleanField(default=False)),
                ('numbering', models.IntegerField(default=0)),
                ('steplist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumtoolHome.Steplist')),
            ],
        ),
        migrations.AddField(
            model_name='steplist',
            name='taskCard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumtoolHome.TaskCard'),
        ),
    ]