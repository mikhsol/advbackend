from django.urls import path

from .views import viewer_count, avg_age

app_name = 'stats-app'

urlpatterns = [
    path('viewer-count/', viewer_count, name='viewer-count'),
    path('avg_age/', avg_age, name='avg-age'),
]
