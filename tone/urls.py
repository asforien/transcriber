from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^resume$', views.resume, name='resume'),
    url(r'^survey$', views.survey, name='survey'),
    url(r'^end$', views.end, name='end'),
    url(r'^summary/([0-9]+)$', views.summary, name='summary'),
    url(r'^([0-9]+)/([0-9]+)$', views.transcribe, name='transcribe'),

    # Redirects for old URLs
    url(r'^alt$', views.alt_start, name='alt_start'),
    url(r'^summary$', views.summary_0, name='summary_0'),
    url(r'^alt/summary$', views.summary_1, name='summary_1'),
]
