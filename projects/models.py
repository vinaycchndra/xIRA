from django.db import models
from accounts.models import Account, ProjectManager

choices = [
    ('Web Development', 'Web Development'),
    ('Software Development', 'Software Development'),
    ('Machine Learning Project', 'Machine Learning Project'),
]


class Project(models.Model):
    project_name         = models.CharField(max_length=30)
    project_description  = models.TextField(max_length=600, blank=True)
    project_category     = models.CharField(max_length=30, choices=choices)
    project_manager      =  models.ForeignKey(ProjectManager, on_delete=models.SET_NULL, null=True)
    assignees            =  models.ManyToManyField(Account)
    start_date           = models.DateTimeField(auto_now_add=True)
    estimated_end_date   = models.DateTimeField()

    def __str__(self):
        return self.project_name






