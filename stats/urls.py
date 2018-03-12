from django.urls import path

from .views import viewer_count, avg_age, gender_dist

app_name = 'stats-app'

urlpatterns = [
    path('viewer-count/', viewer_count, name='viewer-count'),
    path('avg-age/', avg_age, name='avg-age'),
    path('gender-dist/', gender_dist, name='gender-dist'),
]
