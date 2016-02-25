from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^alt$', views.alt_start, name='alt_start'),
    url(r'^alt/survey$', views.alt_survey, name='alt_survey'),
    url(r'^alt/(.+)/(.+)$', views.alt_transcribe, name='alt_transcribe'),
    url(r'^alt/summary$', views.alt_summary, name='alt_summary'),

    url(r'^$', views.start, name='start'),
    url(r'^resume$', views.resume, name='resume'),
    url(r'^survey$', views.survey, name='survey'),
    url(r'^(.+)/(.+)$', views.transcribe, name='transcribe'),
    url(r'^end', views.end, name='end'),
    url(r'^summary', views.summary, name='summary'),
]
