# calendarcore/models.py

from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shift(models.Model):
    MORNING = 'morning'
    EVENING = 'evening'
    TIME_CHOICES = [
        (MORNING, 'Morning'),
        (EVENING, 'Evening'),
    ]

    date = models.DateField()
    time_of_day = models.CharField(max_length=10, choices=TIME_CHOICES)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.time_of_day}"
