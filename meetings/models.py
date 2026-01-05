from django.db import models

class Meeting(models.Model):
    MEETING_TYPE_CHOICES = (
        ('standup', 'Daily Standup'),
        ('review', 'Weekly Review'),
    )
    type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES)
    date_time = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} - {self.date_time}"