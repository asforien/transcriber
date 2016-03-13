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

	interface = subject.interface
	practice_template = 'number_practice.html' if interface == 0 else 'feature_practice.html'
	transcribe_template = 'number_transcribe.html' if interface == 0 else 'feature_transcribe.html'

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
			t = threading.Thread(target=send_email, args=[subject])
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
		return render(request, practice_template, context)
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
		return render(request, transcribe_template, context)

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

		if (done == 0):
			return HttpResponseRedirect('/tone/' + str(sub.pk) + '/0')
		elif (done < 3):
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
		name = name.decode('unicode-escape')
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

		# Use new interface if subject falls within one of the following language groups
		# Or if they speak cantonese
		new_interface_languages = ['English', 'Mandarin', 'Vietnamese']
		interface = 0
		if dominantLanguage in new_interface_languages or targetLanguage == True:
			interface = 1

		sub = Subject.objects.create(name=name, email=email, dominant_language=dominantLanguage,
			other_languages=otherLanguages, target_language=targetLanguage, gender=gender, age=age, question_order=questionOrder, interface=interface)

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

def summary(request, interface):
	subject_list = []
	language_groups = {}
	answer_key = Audio.objects.values_list('answer', flat=True)

	for sub in Subject.objects.filter(interface=interface):
		transcriptions = get_transcriptions(sub)
		if not transcriptions:
			continue

		correct = 0
		total = 0
		time = 0
		q1q2_correct = 0
		q1q2_total = 0
		correct_by_tone = [0] * 6
		total_by_tone = [0] * 6
		for t in transcriptions:
			time += t[2]
			qn = t[0] - 1 # zero-based indexing
			result = t[1]

			# pad result with zeroes to match answer key length for zipping
			if len(result) < len(answer_key[qn]):
				result += '0' * (len(result) - len(answer_key[qn]))

			for c, a in zip(result, answer_key[qn]):
				tone_number = int(a) - 1
				if c == a:
					correct += 1
				if qn == 0 or qn == 1:
					total_by_tone[tone_number] += 1
					if c == a:
						q1q2_correct += 1
						correct_by_tone[tone_number] += 1

			total += len(answer_key[qn])
			if qn == 0 or qn == 1:
				q1q2_total += len(answer_key[qn])

		score = correct / total

		subject_list.append({
			'subject': sub,
			'score': int(score * 100),
			'time': time,
		})

		dl = sub.dominant_language
		if dl not in language_groups:
			language_groups[dl] = {
				'name': dl,
				'subjects': 0,
				'correct': 0,
				'total': 0,
				'q1q2_correct': 0,
				'q1q2_total': 0,
				'correct_by_tone': [0] * 6,
				'total_by_tone': [0] * 6,
				'time': 0,
				'scores': [],
			}

		lg = language_groups[dl]
		lg['subjects'] += 1
		lg['correct'] += correct
		lg['total'] += total
		lg['q1q2_correct'] += q1q2_correct
		lg['q1q2_total'] += q1q2_total
		for i in range(0,6):
			lg['correct_by_tone'][i] += correct_by_tone[i]
			lg['total_by_tone'][i] += total_by_tone[i]
		lg['time'] += time
		lg['scores'].append(score)

	language_group_list = []

	for lang in language_groups:
		lg = language_groups[lang]
		lg['score'] = int(lg['correct'] / lg['total'] * 100)
		lg['q1q2_score'] = int(lg['q1q2_correct'] / lg['q1q2_total'] * 100)
		lg['time'] = lg['time'] // lg['subjects']
		lg['score_by_tone'] = [int(x / y * 100) for x, y in zip(lg['correct_by_tone'], lg['total_by_tone'])]
		language_group_list.append(language_groups[lang])

		scores = lg['scores']
		avg_score = sum(scores)/len(scores)
		variance = 0
		for score in scores:
			diff = score - avg_score
			variance += diff * diff
		std_dev = (variance / len(scores)) ** 0.5
		lg['std_err'] = "{0:.4f}".format(std_dev / (len(scores) ** 0.5))

	subject_list = sorted(subject_list, key=lambda k: k['score'], reverse=True)
	subject_list = sorted(subject_list, key=lambda k: k['subject'].dominant_language)
	language_group_list = sorted(language_group_list, key=lambda k: k['score'], reverse=True)

	context = {
		'subjects': subject_list,
		'language_groups': language_group_list,
	}

	return render(request, 'summary.html', context)

def get_score(sub):

	correct = 0
	total = 0
	time = 0
	for t in Transcription.objects.filter(subject=sub):
		correct += t.score
		total += t.audio.numSegments
		time += t.timeTaken

	return (correct, total, time)

def get_transcriptions(sub):

	results = []
	for t in Transcription.objects.filter(subject=sub):
		results.append((
			t.audio.id,
			t.result,
			t.timeTaken
		))
	return results

def send_email(sub):

	correct, total, time = get_score(sub)
	score = str(int(correct / float(total) * 100)) + '%'

	import smtplib
	fromaddr = 'jeremy.yapjl@gmail.com'
	toaddr  = sub.email.strip()
	msg = "\r\n".join([
		"From: jeremy.yapjl@gmail.com",
		"To: " + sub.email,
		"Subject: Cantonese Tone Recognition Experiment",
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