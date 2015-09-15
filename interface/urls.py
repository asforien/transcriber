from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tone/$', views.toneStart, name='toneStart'),
    url(r'^tone/(.+)$', views.toneFeature, name='toneFeature'),
    url(r'^(.+)/(.+)$', views.binaryFeature, name='binaryFeature'),
    url(r'^end', views.end, name='end'),
]
