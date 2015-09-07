from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(.+)/tone$', views.toneFeature, name='toneFeature'),
    url(r'^(.+)/(.+)$', views.binaryFeature, name='binaryFeature'),
]
