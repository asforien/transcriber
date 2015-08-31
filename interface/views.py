from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

import os
from django.conf import settings
from .models import Audio

def index(request, audio_file, distinctive_feature):
	#if not Audio.objects.all().filter(file_path=audio_file).exists():
	#	return HttpResponseNotFound('<h1>Audio file not found</h1>')

	module_dir = os.path.dirname(__file__)  # get current directory
	alignments_file_path = os.path.join(module_dir, 'static/data/alignments/' + audio_file + '.json')
	alignments = open(alignments_file_path, 'r').read()
	context = {
		'audio_file_path': 'data/audio/' + audio_file + '.mp3',
		'alignments': alignments,
		'distinctive_feature_template': distinctive_feature + '.html',
	}
	return render(request, 'index.html', context)