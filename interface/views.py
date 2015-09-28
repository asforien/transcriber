from django.shortcuts import render
from .models import Transcription, Subject

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings

import csv

def toneFeature(request, audio_file):

	if request.method == 'POST':
		result = request.POST.get('result', '')
		email = request.POST.get('subjectKey', '')
		subject = Subject.objects.get(pk=email)

		Transcription.objects.create(subject=subject, audio=audio_file, result=result)

		if int(audio_file) < 30:
			return HttpResponseRedirect('/transcribe/tone/'  + str(int(audio_file) + 1))
		else:
			return HttpResponseRedirect('/transcribe/end')

	else:
		alignments_file_path = settings.STATIC_ROOT + '/data/alignments/' + audio_file + '.json'
		alignments = open(alignments_file_path, 'r').read()
		context = {
			'audio_file_path': 'data/audio/' + audio_file + '.wav',
			'audio_file_name': audio_file,
			'alignments': alignments,
		}
		return render(request, 'cantoneseTones.html', context)

def start(request):

	return render(request, 'toneStart.html')

def survey(request):

	if request.method == 'POST':
		name = request.POST.get('inputName', '')
		email = request.POST.get('inputEmail', '')
		nativeLanguages = request.POST.get('nativeLanguages', '')
		otherLanguages = request.POST.get('otherLanguages', '')
		targetLanguage = request.POST.get('targetLanguage', '') == 'on'
		gender = request.POST.get('gender', '')
		age = request.POST.get('age', '')

		Subject.objects.create(name=name, email=email,
			nativeLanguages=nativeLanguages,
			otherLanguages=otherLanguages,
			targetLanguage=targetLanguage,
			gender=gender, age=age)

		return HttpResponseRedirect('/transcribe/tone/1')

	else:
		return render(request, 'survey.html')

def end(request):

	return render(request, 'end.html')

def results(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'

    writer = csv.writer(response)
    writer.writerow(['Subject', 'Audio', 'Transcription'])

    for o in Transcription.objects.all():
        writer.writerow([o.subject.email, o.audio, o.result])

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