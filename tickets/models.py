from django.db import models
from projects.models import Project
from accounts.models import Account
import datetime

status_field = (('Backlog', 'Backlog'),
                ('Open', 'Open'),
                ('In Progress', 'In Progress'),
                ('Complete', 'Complete'),
                )

priority_field = (('High', 'High'),
                  ('Medium', 'Medium'),
                  ('Low', 'Low'),
                  ('Lowest', 'Lowest'),
                  )

task_type_choices=(('Bug', 'Bug'), ('New Task', 'New Task'))


class Task(models.Model):
    project       = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_type     = models.CharField(max_length=30, choices = task_type_choices)
    short_summary = models.CharField(max_length=80)
    description   = models.TextField(max_length=500)
    assignee     = models.ForeignKey(Account, on_delete=models.CASCADE)
    status        = models.CharField(max_length=25, choices=status_field)
    priority      = models.CharField(max_length=25, choices=priority_field)
    start_date    = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField()

    def __str__(self):
        return self.short_summary

    # Look for task as backlog
    def task_as_back_log(self):
        current_time = datetime.datetime.now().astimezone()
        estimated_end_date = self.estimated_end_date.astimezone()
        if self.status == 'Complete':
            return False
        if current_time >= estimated_end_date:
            self.status = 'Backlog'
            self.save()
            return True
        else:
            return False

    def get_status_choices(self):
        status = self.status
        if status == 'Open':
            return 'In Progress', 'In Progress'
        else:
            return 'Complete', 'Complete'






