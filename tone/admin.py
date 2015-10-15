from django.contrib import admin

from .models import Transcription, Subject, Audio

admin.site.register(Transcription)
admin.site.register(Subject)
admin.site.register(Audio)
