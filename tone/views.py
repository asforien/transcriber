from django.shortcuts import render
from .models import Transcription, Subject, Audio

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings

import csv
import re
import threading

from Crypto.PublicKey import RSA
from base64 import b64decode

def transcribe(request, subjectId, questionId):

	subject = Subject.objects.get(pk=subjectId)
	audioId = subject.question_order.split(',')[int(questionId) - 1]
	audio = Audio.objects.get(pk=audioId)

	if request.method == 'POST':
		result = request.POST.get('result', '')
		timeTaken = request.POST.get('timeTaken', '')

		score = 0
		for c, a in zip(result, audio.answer):
			if c == a:
				score += 1

		Transcription.objects.update_or_create(subject=subject, audio=audio,
			defaults={'result': result, 'timeTaken': timeTaken, 'score': score})

		if int(questionId) == 3:
			t = threading.Thread(target=sendemail, args=[subject])
			t.setDaemon(False)
			t.start()
			return HttpResponseRedirect('/tone/end')
		else:
			return HttpResponseRedirect('/tone/' + subjectId + '/' + str(int(questionId) + 1))

	elif questionId == '0':

		alignments_file_path = settings.STATIC_ROOT + '/data/alignments/0.json'
		alignments = open(alignments_file_path, 'r').read()

		context = {
			'subject_id': subjectId,
			'audio_file_path': 'data/audio/0.wav',
			'alignments': alignments,
		}
		return render(request, 'practice.html', context)
	else:

		try:
			previous_transcription = Transcription.objects.get(subject=subject, audio=audio)
		except:
			previous_transcription = None
			print("Error")

		previous_answer = None
		if previous_transcription:
			previous_answer = previous_transcription.result

		alignments_file_path = settings.STATIC_ROOT + '/data/alignments/' + audioId + '.json'
		alignments = open(alignments_file_path, 'r').read()
		context = {
			'audio_file_path': 'data/audio/' + audioId + '.wav',
			'subject_id': subjectId,
			'question_id': questionId,
			'prev_qn_id': str(int(questionId)-1),
			'alignments': alignments,
			'answers': previous_answer,
		}
		return render(request, 'toneNumber.html', context)

def start(request):

	return render(request, 'start.html')

def resume(request):

	if request.method == 'POST':
		cipherEmail = request.POST.get('encryptedEmail', '')
		f = open(settings.STATIC_ROOT + '/rsa/private_key.pem', 'r')
		key = RSA.importKey(f.read())
		email = key.decrypt(b64decode(cipherEmail))
		email = email.decode('utf-8').replace('\0', '').encode('utf-8')

		if Subject.objects.filter(email=email).count() == 0:
			return  render(request, 'resume.html',
				{'error': 'No session with the provided email address was found.'})

		sub = Subject.objects.get(email=email)
		done = Transcription.objects.filter(subject=sub).count()

		if (done < 3):
			return HttpResponseRedirect('/tone/' + str(sub.pk) + '/' + str(done + 1))
		else:
			return HttpResponseRedirect('/tone/end')
	else:
		return render(request, 'resume.html')

def survey(request):

	if request.method == 'POST':
		cipherName = request.POST.get('encryptedName', '')
		cipherEmail = request.POST.get('encryptedEmail', '')
		dominantLanguage = request.POST.get('dominantLanguage', '')
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

		if Subject.objects.filter(email=email).count() != 0:
			return render(request, 'resume.html',
				{'error': 'There is already a session with the provided email address.'})

		# Generate questions for subject

		assignedQns = (Subject.objects.filter(dominant_language=dominantLanguage)
			.values_list('question_order', flat="True").distinct())
		
		num_questions = Audio.objects.all().count()

		times_question_used = [0] * (num_questions + 1)
		for qs in assignedQns:
			times_question_used[int(qs.split(',')[2])] += 1

		q3 = 3
		for i in range(4, num_questions + 1):
			if times_question_used[i] < times_question_used[q3]:
				q3 = i

		if Subject.objects.all().count() % 2 == 0:
			questionOrder = "1,2," + str(q3)
		else:
			questionOrder = "2,1," + str(q3)

		sub = Subject.objects.create(name=name, email=email, dominant_language=dominantLanguage,
			other_languages=otherLanguages, target_language=targetLanguage, gender=gender, age=age, question_order=questionOrder)

		return HttpResponseRedirect('/tone/' + str(sub.pk) + '/0')

	else:
		defaultLanguages = ['English', 'Mandarin']
		languages = Subject.objects.values_list('dominant_language', flat=True).distinct()
		languageSet = set(languages)
		languageSet.discard("Testing")
		languages = list(set(defaultLanguages) | languageSet)
		context = {
			'DLs': languages
		}
		return render(request, 'survey.html', context)

def end(request):

	return render(request, 'end.html')

def summary(request):
	entries = []
	for sub in Subject.objects.all():
		correct, total, time = getscore(sub)

		if total == 0:
			continue

		entries.append({
			'subject': sub,
			'score': str(int(correct / float(total) * 100)) + '%',
			'time': time,
		})
	entries = sorted(entries, key=lambda k: k['score'], reverse=True) 

	context = {
		'entries': entries
	}

	return render(request, 'summary.html', context)

def getscore(sub):

	correct = 0
	total = 0
	time = 0
	for t in Transcription.objects.filter(subject=sub):
		correct += t.score
		total += t.audio.numSegments
		time += t.timeTaken

	return (correct, total, time)

def sendemail(sub):

	correct, total, time = getscore(sub)
	score = str(int(correct / float(total) * 100)) + '%'

	import smtplib
	fromaddr = 'jeremy.yapjl@gmail.com'
	toaddr  = sub.email
	msg = "\r\n".join([
		"From: jeremy.yapjl@gmail.com",
		"To: " + sub.email,
		"Subject: Experiment Results & Payment",
		"",
		"Hi " + sub.name + ",",
		"",
		"Thanks for participating in our experiment!",
		"Your score for the experiment was " + str(correct) + "/" + str(total) + " (" + score + ")" + ".",
		"Please let us know your preferred payment method (e.g. PayPal, bank transfer, or meet-up) so that we can process your reimbursement.",
		"If you would not like to be reimbursed, you can choose to refuse payment as well.",
		"",
		"If you know anyone who might be interested to participate in the experiment, please share the experiment URL with them:",
		"http://transcriber.elasticbeanstalk.com",
		"",
		"Thanks",
		"Jeremy",
		])
	username = 'jeremy.yapjl@gmail.com'
	password = 'nclexeijhedptgdq'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddr, msg)
	server.quit()