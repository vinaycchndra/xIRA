from django.db import models
from accounts.models import Account, ProjectManager

choices = (
    ('Web_Development', 'Web Application'),
    ('Software_Development', 'Software Packages'),
    ('Machine Learning Project', 'Data Science Project'),
)


class Project(models.Model):
    project_name         = models.CharField(max_length=30)
    project_description  = models.TextField(max_length=600, blank=True)
    project_category     = models.CharField(max_length=30, choices=choices)
    project_manager      =  models.ForeignKey(ProjectManager, on_delete=models.SET_NULL, null=True)
    assignees            =  models.ManyToManyField(Account,)
    start_date           = models.DateTimeField(auto_now_add=True)
    estimated_end_date   = models.DateTimeField()

    def __str__(self):
        return self.project_name


status_field = (('Backlog', 'back-log'),
                ('In Progress', 'in-progress'),
                ('Complete', 'complete'),
                )

priority_field = (('High', 'high'),
                  ('Medium', 'medium'),
                  ('Low', 'low'),
                  ('Lowest', 'lowest'),
                  )


class Task(models.Model):
    project       = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_type     = models.CharField(max_length=30, choices=(('Bug', 'bug'), ('New Task', 'new task')))
    short_summary = models.CharField(max_length=20)
    description   = models.TextField(max_length=500)
    assignees     = models.ManyToManyField(Account)
    status        = models.CharField(max_length=25, choices=status_field)
    priority      = models.CharField(max_length=25, choices=priority_field)
    start_date    = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField()

    def __str__(self):
        return self.short_summary


