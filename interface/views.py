from django.shortcuts import render
from .models import Transcription, Subject, Audio

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings

import csv
import re

from Crypto.PublicKey import RSA
from base64 import b64decode

def toneFeature(request, audioId):

	if request.method == 'POST':
		result = request.POST.get('result', '')
		subId = request.POST.get('subId', '')
		timeTaken = request.POST.get('timeTaken', '')
		subject = Subject.objects.get(pk=subId)
		audio = Audio.objects.get(pk=audioId)

		score = 0
		for c, a in zip(result, audio.answer):
			if c == a:
				score += 1

		Transcription.objects.create(subject=subject, audio=audio,
			result=result, timeTaken=timeTaken, score=score, choiceType=0)

		if int(audioId) < 30:
			return HttpResponseRedirect('/transcribe/tone/'  + str(int(audioId) + 1))
		else:
			return HttpResponseRedirect('/transcribe/end')

	else:
		Transcription.objects.filter(pk=1).delete()
		alignments_file_path = settings.STATIC_ROOT + '/data/alignments/' + audioId + '.json'
		alignments = open(alignments_file_path, 'r').read()
		context = {
			'audio_file_path': 'data/audio/' + audioId + '.wav',
			'audio_file_name': audioId,
			'alignments': alignments,
		}
		return render(request, 'cantoneseTones.html', context)

def start(request):

	return render(request, 'toneStart.html')

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
		print(key)
		name = key.decrypt(b64decode(cipherName))
		email = key.decrypt(b64decode(cipherEmail))
		name = name.decode('utf-8').replace('\0', '').encode('utf-8')
		email = email.decode('utf-8').replace('\0', '').encode('utf-8')

		subject = Subject.objects.create(name=name, email=email,
			nativeLanguages=nativeLanguages,
			otherLanguages=otherLanguages,
			targetLanguage=targetLanguage,
			gender=gender, age=age)

		context = {
			'subId': subject.pk,
		}
		return render(request, 'saveCookie.html', context)

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
			'score': score / float(total),
			'time': time,
		})
	entries = sorted(entries, key=lambda k: k['score'], reverse=True) 

	context = {
		'entries': entries
	}

	return render(request, 'summary.html', context)

def results(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'

    writer = csv.writer(response)
    writer.writerow(['Subject', 'Audio', 'Transcription'])

    for o in Transcription.objects.all():
        writer.writerow([o.subject.pk, o.audio, o.result])

    return response

# def binaryFeature(request, distinctive_feature, audio_file):

# 	module_dir = os.path.dirname(__file__)  # get current directory
# 	alignments_file_path = settings.STATIC_ROOT + 'data/alignments/' + audio_file + '.json'
# 	alignments = open(alignments_file_path, 'r').read()
# 	context = {
# 		'audio_file_path': 'data/audio/' + audio_file + '.wav',
# 		'audio_file_name': audio_file,
# 		'alignments': alignments,
# 		'distinctive_feature_template': distinctive_feature + '.html',
# 	}
# 	return render(request, 'binaryFeature.html', context)