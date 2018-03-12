from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from .models import (
    Event,
    Device,
    Content,
    Person
)

@require_GET
def viewer_count(request):
    data = prepare_viewe_count_params(request.GET)
    device = Device.objects.get(pk=data['device_id'])
    content = Content.objects.get(pk=data['content_id'])
    start = parse_datetime(data['start'])
    end = parse_datetime(data['end'])
    if isSuchEvent(device, content, start, end):
        data['views'] = len(Person.objects.filter(device=device,
            appears__gte=start, disappears__lte=end))

    return JsonResponse(data, status=200)

def isSuchEvent(device, content, start, end):
    return len(Event.objects.filter(device=device, content=content,
            event_time__gte=start, event_time__lte=end)) > 0

def prepare_viewe_count_params(params):
    return {'device_id': int(params['device']),
        'content_id': int(params['content']),
        'start': params['start'],
        'end': params['end'],
        'views': 0}