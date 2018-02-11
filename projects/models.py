from datetime import date, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Project(models.Model):
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='projects')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(default=date.today, blank=True)
    end_date = models.DateField(default=date.today, blank=True)
    in_work = models.BooleanField(default=False)


    class Meta:
        ordering = ('end_date',)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('project_detail_view', kwargs={'pk': self.pk})


class List(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='lists')


    def __str__(self):
        return f'{self.id}'


class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    is_done = models.BooleanField(default=False)


    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


    def __str__(self):
        return self.text


class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    is_done = models.BooleanField(default=False)


    class Meta:
        ordering = ('-datetime',)


    def __str__(self):
        return self.name


class WorkDay(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_days')
    start_time = models.DateTimeField(null=True)
    elapsed_time = models.DurationField(default=timedelta(0), null=True)
    date = models.DateField(default=date.today, primary_key=True)
    in_work = models.BooleanField(default=False)


    def __str__(self):
        return str(self.date)


    def start_working(self):
        self.in_work = True
        self.start_time = timezone.now()
        self.save()


    def stop_working(self):
        self.in_work = False
        work_time = timezone.now() - self.start_time
        self.elapsed_time += work_time
        self.save()
