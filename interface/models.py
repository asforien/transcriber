from django.db import models

class Audio(models.Model):
	file_path = models.CharField(max_length=200)

	def __str__(self):
		return self.file_path

class DistinctiveFeature(models.Model):
	name = models.CharField(max_length=30)

class Transcription(models.Model):
	audio = models.ForeignKey(Audio)
	distinctive_feature = models.ForeignKey(DistinctiveFeature)
	result = models.CharField(max_length=30)

	def __str__(self):
		return self.distinctive_feature.name + ": " + result