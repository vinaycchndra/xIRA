from django.db import models
from projects.models import Project
from accounts.models import Account

status_field = (('Backlog', 'back-log'),
                ('Not Started', 'not-started'),
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
    short_summary = models.CharField(max_length=80)
    description   = models.TextField(max_length=500)
    assignees     = models.ManyToManyField(Account)
    status        = models.CharField(max_length=25, choices=status_field)
    priority      = models.CharField(max_length=25, choices=priority_field)
    start_date    = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField()

    def __str__(self):
        return self.short_summary
