from django.contrib import admin

from .models import Audio
from .models import Transcription

admin.site.register(Audio)
admin.site.register(Transcription)
