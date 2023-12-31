# Generated by Django 4.2.2 on 2023-06-29 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('Bug', 'bug'), ('New Task', 'new task')], max_length=30)),
                ('short_summary', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('Backlog', 'back-log'), ('In Progress', 'in-progress'), ('Complete', 'complete')], max_length=25)),
                ('priority', models.CharField(choices=[('High', 'high'), ('Medium', 'medium'), ('Low', 'low'), ('Lowest', 'lowest')], max_length=25)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('estimated_end_date', models.DateTimeField()),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
