from django.db import models
from accounts.models import User

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    yesterday = models.TextField()
    today = models.TextField()
    blockers = models.TextField(blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
