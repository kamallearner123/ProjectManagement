from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    scope = models.TextField()

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    java_score = models.IntegerField()
    sql_score = models.IntegerField()
    team_fit = models.IntegerField()

    @property
    def total_score(self):
        return self.java_score + self.sql_score + self.team_fit

    def __str__(self):
        return self.name
