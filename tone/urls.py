from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^resume$', views.resume, name='resume'),
    url(r'^survey$', views.survey, name='survey'),
    url(r'^(.+)/(.+)$', views.transcribe, name='transcribe'),
    url(r'^end', views.end, name='end'),
    url(r'^summary', views.summary, name='summary'),
]
