from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from .models import (
    Event,
    Device,
    Content,
    Person
)


def get_set_of_persons(events, device):
    list_of_persons_lists = [Person.objects.filter(
                        device=device,
                        appears__lte=events[i].event_time,
                        disappears__gte=events[i+1].event_time)
                for i in range(0, len(events), 2)]
    return set([person for sublist in list_of_persons_lists
                for person in sublist])


def preprocess_events(events):
    # Will count only persons who watch whole content from start to end
    # that's why if first event is 'end' can't process this event and
    # remove it from list
    if events[0].event_type == 'end':
        del events[0]
    # If length of events list not even, than I have 'start' point of last
    # event but have no endpoint, can't process this event and
    # remove it from list
    if len(events) % 2 != 0:
        del events[len(events)-1]
    return events


def prepare_params(data):
    return Device.objects.get(pk=data['device_id']), \
           Content.objects.get(pk=data['content_id']), \
           parse_datetime(data['start']), parse_datetime(data['end'])


def prepare_data(params):
    return {
        'device_id': int(params['device']),
        'content_id': int(params['content']),
        'start': params['start'],
        'end': params['end'],
    }


def get_persons(data):
    device, content, start, end = prepare_params(data)
    # Get ordered list of filtered events, assume all data is correct which
    # means all events with same content and device id will not intersects and
    # all events types in list will be alternate (start, finish, ...) and will
    # no have start, start or finish, finish sequences.
    events = list(Event.objects.filter(
        device=device, content=content, event_time__gte=start,
        event_time__lte=end).order_by('event_time'))
    # Check if such events exists, if yes - process it
    if len(events) > 0:
        events = preprocess_events(events)
        return get_set_of_persons(events, device)
    else:
        return set()


@require_GET
def viewer_count(request):
    data = prepare_data(request.GET)
    persons = get_persons(data)
    data['views'] = len(persons)

    return JsonResponse(data, status=200)


@require_GET
def avg_age(request):
    data = prepare_data(request.GET)
    persons = get_persons(data)

    if len(persons) > 0:
        data['avg_age'] = round(
            float(sum([p.age for p in persons])) / len(persons), 1)
    else:
        data['avg_age'] = 'No persons for events'

    return JsonResponse(data, status=200)
