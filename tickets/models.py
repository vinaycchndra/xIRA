from django.db import models
from projects.models import Project
from accounts.models import Account

status_field = (('back-log', 'Backlog'),
                ('open', 'Open'),
                ('in-progress', 'In Progress'),
                ('complete', 'Complete'),
                )

priority_field = (('high', 'High'),
                  ('medium', 'Medium'),
                  ('low', 'Low'),
                  ('lowest', 'Lowest'),
                  )


class Task(models.Model):
    project       = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_type     = models.CharField(max_length=30, choices=(('bug', 'Bug'), ('new task', 'New Task')))
    short_summary = models.CharField(max_length=80)
    description   = models.TextField(max_length=500)
    assignee     = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    status        = models.CharField(max_length=25, choices=status_field)
    priority      = models.CharField(max_length=25, choices=priority_field)
    start_date    = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField()

    def __str__(self):
        return self.short_summary
