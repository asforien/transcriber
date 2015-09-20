from django.db import models

class Transcription(models.Model):
	audio = models.IntegerField()
	result = models.CharField(max_length=30)

	def __str__(self):
		return audio + ", " + result