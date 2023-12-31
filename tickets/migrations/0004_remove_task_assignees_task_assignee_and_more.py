# Generated by Django 4.2.2 on 2023-06-30 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0003_alter_task_short_summary_alter_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assignees',
        ),
        migrations.AddField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), ('lowest', 'Lowest')], max_length=25),
        ),
    ]
