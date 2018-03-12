from django.db import models


class Device(models.Model):
    pass


class Content(models.Model):
    pass


class Event(models.Model):
    EVENT_TYPES = (
        ('start', 'Event start timestamp'),
        ('end', 'Event end timestamp')
    )

    content = models.ForeignKey('Content', related_name='event_content',
        on_delete=models.CASCADE)
    device = models.ForeignKey('Device', related_name='event_device',
        on_delete=models.CASCADE)
    event_type = models.CharField(max_length=5, choices=EVENT_TYPES)
    event_time = models.DateTimeField()


class Person(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    device = models.ForeignKey('Device', related_name='person_device',
        on_delete=models.CASCADE)
    appears = models.DateTimeField()
    disappears = models.DateTimeField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER)
