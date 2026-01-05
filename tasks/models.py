from django.db import models
from accounts.models import User
from core.models import Project

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    week = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    metrics = models.JSONField(default=dict)
    dependencies = models.ManyToManyField('self', blank=True, symmetrical=False)
    duration = models.IntegerField(help_text='Duration in days')

    def __str__(self):
        return self.title
