# Generated by Django 5.1.7 on 2025-03-09 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ResearchProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('niche', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('planning', 'Planning'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='planning', max_length=20)),
                ('progress', models.PositiveSmallIntegerField(default=0, help_text='Progress percentage (0-100)')),
                ('department_requirement', models.CharField(blank=True, max_length=100)),
                ('skills_required', models.TextField(blank=True, help_text='Comma-separated list of required skills')),
                ('max_students', models.PositiveSmallIntegerField(default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
