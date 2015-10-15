from django.db import models

class Subject(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	native_languages = models.CharField(max_length=255)
	other_languages = models.CharField(max_length=255)
	target_language = models.BooleanField(default=False)
	gender = models.CharField(max_length=10)
	age = models.IntegerField(default=0)
	question_order = models.CharField(max_length=255)

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
	fileName = models.CharField(max_length=255)
	numSegments = models.IntegerField()
	answer = models.CharField(max_length=255)

	def __str__(self):
		return str(self.id)