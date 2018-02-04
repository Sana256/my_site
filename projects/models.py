from datetime import date

from django.db import models
from django.conf import settings
from django.utils import timezone


class Project(models.Model):
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    in_work = models.BooleanField(default='False')


    class Meta:
        ordering = ('-end_date',)


    def __str__(self):
        return self.name


class List(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, related_name='lists')


    def __str__(self):
        return self.id


class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.TextField(default='', blank=False)
    is_done = models.BooleanField(default='False')


    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


    def __str__(self):
        return self.text


class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, related_name='events')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    is_done = models.BooleanField(default='False')


    class Meta:
        ordering = ('-date',)


    def __str__(self):
        return self.name


class WorkDay(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_days')
    start_time = models.DateTimeField(default=timezone.now)
    elapsed_time = models.DurationField()
    date = models.DateField(default=date.today)
    in_work = models.BooleanField(default=False)
