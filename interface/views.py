from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request, audio_file, distinctive_feature):
	context = {
		'audio_file_path': 'media/' + audio_file + '.mp3',
		'segments': '1',
		'distinctive_feature': distinctive_feature,
	}
	return render(request, 'index.html', context)