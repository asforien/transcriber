from django.db import models

class Subject(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	dominant_language = models.CharField(max_length=25)
	other_languages = models.CharField(max_length=255, blank=True)
	target_language = models.BooleanField(default=False)
	gender = models.CharField(max_length=10)
	age = models.IntegerField(default=0)
	question_order = models.CharField(max_length=25)

	def __str__(self):
		return self.name + ":" + self.email

class Transcription(models.Model):
	subject = models.ForeignKey('Subject')
	audio = models.ForeignKey('Audio')
	result = models.CharField(max_length=40)
	timeTaken = models.IntegerField()
	score = models.IntegerField()

	def __str__(self):
		return self.subject.name + ":" + str(self.audio.id)

class Audio(models.Model):
	id = models.IntegerField(primary_key=True)
	fileName = models.CharField(max_length=255)
	numSegments = models.IntegerField()
	answer = models.CharField(max_length=255)

	def __str__(self):
		return str(self.id)