from django.test import TestCase

from django.utils.dateparse import parse_datetime
import json
from django.urls import reverse

from . import views

from .models import (
    Device,
    Content,
    Event,
    Person
)


class StatsApiTests(TestCase):

    def setUp(self):
        # Two devices
        d1 = Device.objects.create()
        d2 = Device.objects.create()

        # Three person who look on two devices in intersected periods of time
        p1 = Person.objects.create(
            device=d1,
            appears=parse_datetime('2016-01-01 00:00:01'),
            disappears=parse_datetime('2016-01-01 00:03:06'),
            age=40, gender='female')
        p2 = Person.objects.create(
            device=d1,
            appears=parse_datetime('2016-01-01 00:00:00'),
            disappears=parse_datetime('2016-01-01 00:03:47'),
            age=23, gender='male')
        p3 = Person.objects.create(
            device=d2,
            appears=parse_datetime('2016-01-01 00:00:31'),
            disappears=parse_datetime('2016-01-01 00:01:14'),
            age=44, gender='male')

        # Two contents which displayed on two devices same moment
        c1 = Content.objects.create()
        c2 = Content.objects.create()

        # events of showing the diffrent content on different devices
        e7 = Event.objects.create(
            content=c1,
            device=d1, event_type='end',
            event_time=parse_datetime('2016-01-01 00:00:00'))

        e1 = Event.objects.create(
            content=c1,
            device=d1, event_type='start',
            event_time=parse_datetime('2016-01-01 00:00:01'))
        sele2 = Event.objects.create(
            content=c1,
            device=d1, event_type='end',
            event_time=parse_datetime('2016-01-01 00:01:29'))

        e5 = Event.objects.create(
            content=c1,
            device=d1, event_type='start',
            event_time=parse_datetime('2016-01-01 00:02:01'))
        e6 = Event.objects.create(
            content=c1,
            device=d1, event_type='end',
            event_time=parse_datetime('2016-01-01 00:03:29'))

        e3 = Event.objects.create(
            content=c2,
            device=d2, event_type='start',
            event_time=parse_datetime('2016-01-01 00:00:01'))
        e4 = Event.objects.create(
            content=c2,
            device=d2, event_type='end',
            event_time=parse_datetime('2016-01-01 00:01:29'))

    def test_number_of_viewers(self):
        '''
        Returns the number of viewers of a given device and content in a given
        time period.
        If person see same content on same device several times, will concider
        him/her as one person.
        '''
        url = reverse('stats-app:viewer-count')
        response = self.client.get(url, {
            'start': '2016-01-01 00:00:00',
            'end': '2016-01-01 00:03:30', 'device': 1, 'content': 1})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['start'], '2016-01-01 00:00:00')
        self.assertEqual(data['end'], '2016-01-01 00:03:30')
        self.assertEqual(data['device_id'], 1)
        self.assertEqual(data['content_id'], 1)
        self.assertEqual(data['views'], 2)

    def test_average_age_of_viewers(self):
        '''
        Returns the average age of viewers of a given device and content in a
        given time period.
        If person see same content on same device several times, will concider
        him/her as one person.
        '''
        url = reverse('stats-app:avg-age')
        response = self.client.get(url, {
            'start': '2016-01-01 00:00:00',
            'end': '2016-01-01 00:03:30', 'device': 1, 'content': 1})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['start'], '2016-01-01 00:00:00')
        self.assertEqual(data['end'], '2016-01-01 00:03:30')
        self.assertEqual(data['device_id'], 1)
        self.assertEqual(data['content_id'], 1)
        self.assertEqual(data['avg_age'], 31.5)

    def test_gender_distribution_of_viewers(self):
        '''
        Returns the gender distribution of the viewers of a given device and
        content in a given time period.
        If person see same content on same device several times, will concider
        him/her as one person.
        '''
        url = reverse('stats-app:gender-dist')
        response = self.client.get(url, {
            'start': '2016-01-01 00:00:00',
            'end': '2016-01-01 00:03:30', 'device': 1, 'content': 1})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['start'], '2016-01-01 00:00:00')
        self.assertEqual(data['end'], '2016-01-01 00:03:30')
        self.assertEqual(data['device_id'], 1)
        self.assertEqual(data['content_id'], 1)
        self.assertEqual(data['gender_dist']['male'], .50)
        self.assertEqual(data['gender_dist']['female'], .50)