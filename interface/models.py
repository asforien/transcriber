from django.db import models

class Subject(models.Model):
	name = models.CharField(max_length=255, blank=False)
	email = models.CharField(max_length=255, blank=False)
	nativeLanguages = models.CharField(max_length=255, blank=False)
	otherLanguages = models.CharField(max_length=255)
	targetLanguage = models.BooleanField()
	gender = models.CharField(max_length=10, blank=False)
	age = models.IntegerField()

	def __str__(self):
		return self.name + ":" + self.email

class Transcription(models.Model):
	subject = models.ForeignKey('Subject')
	audio = models.ForeignKey('Audio')
	choiceType = models.IntegerField()
	result = models.CharField(max_length=30)
	timeTaken = models.IntegerField()
	score = models.IntegerField()

	def __str__(self):
		return self.subject.name + ":" + str(self.audio.id) + ":" + str(self.choiceType)

class Audio(models.Model):
	id = models.IntegerField(primary_key=True)
	numSegments = models.IntegerField()
	answer = models.CharField(max_length=255)

	def __str__(self):
		return str(self.id)