from django.db import models
from django.contrib.postgres.fields import ArrayField


class event_type(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    availability = models.IntegerField()
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()

    def __str__(self):
        return self.name


class attendee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    registered_events = models.ManyToManyField(event_type, related_name="attendees")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class waiting_list(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    registered_events = models.ManyToManyField(event_type, related_name="waiting_list")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
