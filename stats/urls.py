from django.urls import path

from .views import viewer_count

app_name = 'stats-app'

urlpatterns = [
    path('viewer-count/', viewer_count, name='viewer-count'),
]
