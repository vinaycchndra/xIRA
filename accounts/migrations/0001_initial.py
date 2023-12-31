# Generated by Django 4.2.2 on 2023-06-25 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('work_email', models.EmailField(max_length=100, unique=True)),
                ('contact_number', models.CharField(max_length=50)),
                ('work_profile', models.CharField(choices=[('Frontend Developer', 'Frontend Developer'), ('Backend Developer', 'Backend Developer'), ('UX Engineer', 'UX Engineer'), ('UX Engineer', 'UX Engineer'), ('Data Scientist', 'Data Scientist'), ('Data Engineer', 'Data Engineer')], max_length=30)),
                ('is_project_manager', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
