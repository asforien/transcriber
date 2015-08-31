import csv
import json
from decimal import *

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

alignmentsByFile = {}
durationsByFile = {}

with open('CA_alignments.txt', 'rb') as inputFile:
	reader = csv.reader(inputFile, delimiter=' ')

	for row in reader:
		fileName = row[0]
		if fileName not in alignmentsByFile:
			alignmentsByFile[fileName] = []

		if int(row[4]) != 1:
			alignmentsByFile[fileName].append([Decimal(row[2]), Decimal(row[3])])

with open('durations', 'rb') as inputFile:
	reader = csv.reader(inputFile, delimiter=' ')

	for row in reader:
		fileName = row[0]
		durationsByFile[fileName] =	[Decimal(x) for x in row[1:]]

for fileName, data in alignmentsByFile.iteritems():

	cutPositions = [0]
	cutPositions.extend(durationsByFile[fileName])
	for i in range(1, len(cutPositions)):
		cutPositions[i] += cutPositions[i-1]

	for part in range(1,5):
		with open('alignments/' + fileName + '-' + str(part) + '.json', 'w') as outputFile:
			alignmentsInRange = [[x[0] + Decimal(0.08) * part + Decimal(0.08), x[1]]
				for x in data]
			alignmentsInRange = [
				[x[0] - cutPositions[part-1], x[1]]
				for x in alignmentsInRange if
				x[0] + x[1] > cutPositions[part-1] and
				(part == 4 or x[0] < cutPositions[part])
			]
			json.dump(alignmentsInRange, outputFile, default=decimal_default)