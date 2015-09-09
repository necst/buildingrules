import json
import os
import sys

def write(fileName, line):
	f = open(fileName,'a')
	f.write(line + "\n") 
	f.close() 

def writeAggregate(label, value):
	line = label + ";" + str(value)
	write("aggregate.csv", line)

def writeDetail(line):
	write("detail.csv", line)


if os.path.exists("aggregate.csv"): os.remove("aggregate.csv")
if os.path.exists("detail.csv"): os.remove("detail.csv")


maxOccupants = sys.maxint
if len( sys.argv ) == 2:
	maxOccupants = int(sys.argv[1])

f = open("results.txt")
lines = f.readlines()
f.close()

keyFilter = ['logicalConflicts', 'runtimeConflicts', 'duplicatedRules']

sumValues = {}
maxVal = {}
minVal = {}

roomCounter = 0
nonZeroCounterAbs = 0
zeroCounterAbs = 0
zeroCounter = {}
for k in keyFilter:
	zeroCounter[k] = 0

for line in lines:
	splittedLine = line.split(";")

	lineNumber = int(splittedLine[0].strip())
	timestamp = splittedLine[1]
	content = splittedLine[2].replace("'",'"').replace("set(","").replace(")","")
	content = json.loads(content)

	if lineNumber == 0:
		for key, value in content.iteritems():

			if key == "consequentStats":
				for k,v in value.iteritems():
					writeAggregate(k,v) 

			elif key == "antecedentStats":
				for k,v in value.iteritems():
					writeAggregate(k,v)
			else:
				writeAggregate(key,value)
	else:
		
		occupants = content["occupants"]

		if occupants > maxOccupants:
			continue;

		if occupants not in sumValues.keys():
			sumValues[occupants] = {}
			for key in keyFilter:
				sumValues[occupants]["cardinality"] = 0
				sumValues[occupants][key] = 0

		if not occupants in minVal.keys():
			minVal[occupants] = {}
			for k in sumValues[occupants].keys():
				if k != "cardinality" :  minVal[occupants][k] = sys.maxint
		
		if not occupants in maxVal.keys():
			maxVal[occupants] = {}
			for k in sumValues[occupants].keys():
				if k != "cardinality" : maxVal[occupants][k] = 0

		

		sumValues[occupants]["cardinality"] += 1
		for key in keyFilter:
			sumValues[occupants][key] += content[key] 

		for k in keyFilter:
			if content[k] < minVal[occupants][k] : minVal[occupants][k] = content[k]
			if content[k] > maxVal[occupants][k] : maxVal[occupants][k] = content[k]

		for k in keyFilter:
			if content[k] == 0: zeroCounter[k] += 1


		zeroKeyFound = True
		for k in keyFilter:
			if k != 'duplicatedRules':
				if content[k] != 0: zeroKeyFound = False
		
		if zeroKeyFound:
			zeroCounterAbs += 1
		else:
			nonZeroCounterAbs += 1

		roomCounter += 1



for k in keyFilter:
	writeAggregate("Number of rooms without " + k, zeroCounter[k])

writeAggregate("Number of rooms without any conflict", zeroCounterAbs)
writeAggregate("Number of rooms with at least one conflict", nonZeroCounterAbs)

writeAggregate("Total number of rooms", roomCounter)

writeDetail("occupants;cardinality;max_logicalConflicts;min_logicalConflicts;avg_logicalConflicts;max_runtimeConflicts;min_runtimeConflicts;avg_runtimeConflicts;max_duplicatedRules;min_duplicatedRules;avg_duplicatedRules;")
for occupants in sumValues.keys():

	for k in keyFilter:
		sumValues[occupants][k] = float(sumValues[occupants][k]) / float(sumValues[occupants]["cardinality"])

	line = str(occupants) + ";" + str(sumValues[occupants]["cardinality"])  + ";"
	for k in keyFilter:
		line += str(maxVal[occupants][k])  + ";" + str(minVal[occupants][k]) + ";" + str(sumValues[occupants][k])  + ";"

	writeDetail(line)




