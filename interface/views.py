from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext, loader

import os
from django.conf import settings
from .models import Audio

def binaryFeature(request, distinctive_feature, audio_file):

	module_dir = os.path.dirname(__file__)  # get current directory
	alignments_file_path = os.path.join(module_dir, 'static/data/alignments/' + audio_file + '.json')
	alignments = open(alignments_file_path, 'r').read()
	context = {
		'audio_file_path': 'data/audio/' + audio_file + '.wav',
		'audio_file_name': audio_file,
		'alignments': alignments,
		'distinctive_feature_template': distinctive_feature + '.html',
	}
	return render(request, 'binaryFeature.html', context)

def toneFeature(request, audio_file):

	if request.method == 'POST':

		module_dir = os.path.dirname(__file__)  # get current directory
		with open(os.path.join(module_dir, 'static/data/transcriptions/' + audio_file + '.txt'), 'w') as outp:
			outp.write(request.POST.get('result', ''))

		if int(audio_file) < 30:
			return HttpResponseRedirect('/transcribe/tone/'  + str(int(audio_file) + 1))
		else:
			return HttpResponseRedirect('/transcribe/done')

	else:
		module_dir = os.path.dirname(__file__)  # get current directory
		alignments_file_path = os.path.join(module_dir, 'static/data/alignments/' + audio_file + '.json')
		alignments = open(alignments_file_path, 'r').read()
		context = {
			'audio_file_path': 'data/audio/' + audio_file + '.wav',
			'audio_file_name': audio_file,
			'alignments': alignments,
		}
		return render(request, 'cantoneseTones.html', context)

def done(request):
	
	return render(request, 'done.html')