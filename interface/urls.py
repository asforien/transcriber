from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tone/$', views.start, name='start'),
    url(r'^tone/survey$', views.survey, name='survey'),
    url(r'^tone/(.+)/(.+)$', views.toneFeature, name='toneFeature'),
    #url(r'^(.+)/(.+)$', views.binaryFeature, name='binaryFeature'),
    url(r'^end', views.end, name='end'),
    url(r'^summary', views.summary, name='summary'),
    url(r'^results/$', views.results, name='results'),
]
