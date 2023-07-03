# Generated by Django 4.2.2 on 2023-07-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_task_assignee_alter_task_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low'), ('Lowest', 'Lowest')], max_length=25),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Backlog', 'Backlog'), ('Open', 'Open'), ('In Progress', 'In Progress'), ('Complete', 'Complete')], max_length=25),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('Bug', 'Bug'), ('New Task', 'New Task')], max_length=30),
        ),
    ]