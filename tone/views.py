from django.shortcuts import render
from .models import Transcription, Subject, Audio

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings

import csv
import re

from Crypto.PublicKey import RSA
from base64 import b64decode

def transcribe(request, subjectId, questionId):

	subject = Subject.objects.get(pk=subjectId)
	qInfo = subject.question_order.split(',')[int(questionId) - 1]
	audioId = qInfo.split('.')[0]
	choiceType = qInfo.split('.')[1]

	if request.method == 'POST':
		result = request.POST.get('result', '')
		timeTaken = request.POST.get('timeTaken', '')

		audio = Audio.objects.get(pk=audioId)

		if choiceType == '2':
			toneMapping = {
				'HL': '1',
				'HR': '2',
				'ML': '3',
				'LF': '4',
				'LR': '5',
				'LL': '6'
			}
			result = [result[i:i+2] for i in range(0, len(result), 2)]
			result = [toneMapping[i] for i in result]
			result = ''.join(result)

		score = 0
		for c, a in zip(result, audio.answer):
			if c == a:
				score += 1

		Transcription.objects.create(subject=subject, audio=audio,
			result=result, timeTaken=timeTaken, score=score, choiceType=choiceType)

		if int(questionId) == 3:
			return HttpResponseRedirect('/tone/end')
		else:
			return HttpResponseRedirect('/tone/' + subjectId + '/' + str(int(questionId) + 1))

	else:
		alignments_file_path = settings.STATIC_ROOT + '/data/alignments/' + audioId + '.json'
		alignments = open(alignments_file_path, 'r').read()
		context = {
			'audio_file_path': 'data/audio/' + audioId + '.wav',
			'subject_id': subjectId,
			'question_id': questionId,
			'alignments': alignments,
		}
		if int(choiceType) == 1:
			template = 'toneNumber.html'
		else:
			template = 'toneFeature.html'
		return render(request, template, context)

def start(request):

	return render(request, 'start.html')

def survey(request):

	if request.method == 'POST':
		cipherName = request.POST.get('encryptedName', '')
		cipherEmail = request.POST.get('encryptedEmail', '')
		nativeLanguages = request.POST.get('nativeLanguages', '')
		otherLanguages = request.POST.get('otherLanguages', '')
		targetLanguage = request.POST.get('targetLanguage', '') == 'on'
		gender = request.POST.get('gender', '')
		age = request.POST.get('age', '')

		f = open(settings.STATIC_ROOT + '/rsa/private_key.pem', 'r')
		key = RSA.importKey(f.read())
		name = key.decrypt(b64decode(cipherName))
		email = key.decrypt(b64decode(cipherEmail))
		name = name.decode('utf-8').replace('\0', '').encode('utf-8')
		email = email.decode('utf-8').replace('\0', '').encode('utf-8')

		subs = Subject.objects.filter(name='')
		s = subs[0]
		s.name = name
		s.email = email
		s.native_languages = nativeLanguages
		s.other_languages = otherLanguages
		s.target_language = targetLanguage
		s.gender = gender
		s.age = age
		s.save()

		return HttpResponseRedirect('/tone/' + str(s.pk) + '/1')

	else:
		return render(request, 'survey.html')

def end(request):

	return render(request, 'end.html')

def summary(request):
	entries = []
	for sub in Subject.objects.all():
		score = 0
		total = 0
		time = 0
		for t in Transcription.objects.filter(subject=sub):
			score += t.score
			total += t.audio.numSegments
			time += t.timeTaken

		if total == 0:
			continue

		entries.append({
			'subject': sub,
			'score': str(int(score / float(total) * 100)) + '%',
			'time': time,
		})
	entries = sorted(entries, key=lambda k: k['score'], reverse=True) 

	context = {
		'entries': entries
	}

	return render(request, 'summary.html', context)