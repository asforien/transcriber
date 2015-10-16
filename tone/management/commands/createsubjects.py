import os

from django.core.management.base import BaseCommand  
from ...models import Subject

class Command(BaseCommand):

	def handle(self, *args, **options):
		if Subject.objects.count() == 0:
			type1 = True
			q2First = False
			for i in range(0, 40):
				q3 = i % 10 + 3

				if q2First:
					qOrder = [2, 2, 1, 1, q3, q3]
				else:
					qOrder = [1, 1, 2, 2, q3, q3]

				if type1:
					types = [1, 2, 1, 2, 1, 2]
				else:
					types = [2, 1, 2, 1, 2, 1]

				qSequence = [ str(x[0]) + '.' + str(x[1]) for x in zip(qOrder, types)]
				qString = ','.join(qSequence) 

				Subject.objects.create(question_order=qString)

				type1 = not type1
				if i % 2 == 0:
					q2First = not q2First