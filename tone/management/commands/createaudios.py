import os

from django.core.management.base import BaseCommand  
from ...models import Audio

class Command(BaseCommand):

	def handle(self, *args, **options):
		audioInfo = [
			[1, 'cantonese_141015_367259-15',	'256662351261343423115414'],
			[2, 'cantonese_140927_363450-6',	'33366255344362253126114436'],
			[3, 'cantonese_140916_361200-30',	'23535636144362463323136516'],
			[4, 'cantonese_140927_363450-5',	'444215614163556266422313'],
		]

		for i in audioInfo:
			Audio.objects.update_or_create(
				id = i[0],
				fileName = i[1],
				numSegments = len(i[2]),
				answer = i[2],
			)