import sys
import copy
import rest
import time
import datetime
import os
import json
import math  

brules_username = "user"
brules_password = "user"
brules_buildingName = "CSE"
brules_userUuid = None
brules_sessionKey = None
brules_roomName =  "100"

resultsLogLine = 0
errorLogLine = 0

#######################################################

antecedentCounter = {}
consequentCounter = {}

def backupResults():

	if os.path.exists("results.txt"):

		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H_%M_%S')
		destination = "results_" + str(st) + ".txt"
		os.rename("results.txt", destination)

def logerror(message):

	global errorLogLine

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	out_file = open("errors.txt","a")
	out_file.write(str(errorLogLine) + ";" + st + " > " + str(message) + "\n\n")
	out_file.close()

	errorLogLine += 1

def saveResults(results):

	global resultsLogLine

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	out_file = open("results.txt","a")
	out_file.write(str(resultsLogLine) + ";" +st + ";" + str(results) + "\n")
	out_file.close()

	resultsLogLine += 1

def translateDay(value):

	if value.upper().startswith("MON"): return str(1)
	if value.upper().startswith("TUE"): return str(2)
	if value.upper().startswith("WED"): return str(3)
	if value.upper().startswith("THU"): return str(4)
	if value.upper().startswith("FRI"): return str(5)
	if value.upper().startswith("SAT"): return str(6)
	if value.upper().startswith("SUN"): return str(7)



def translateRule(rule):

	global antecedentCounter
	global consequentCounter

	splitted = rule.replace("\n","").strip().replace("-","|").split("|")
 	splitted = filter(None, splitted)[1:]


 	antecedent = ""
	if splitted[0].strip() == "someone is in the room" : antecedent = "someone is in the room"
	elif splitted[0].strip() == "nobody is in the room" : antecedent = "nobody is in the room"
	elif splitted[0].strip() == "temperature is between" : antecedent = "room temperature is between"
	elif splitted[0].strip() == "it is between (time)" : antecedent = "time is between"
	elif splitted[0].strip() == "it is between (day)" : antecedent = "the day is between"
	elif splitted[0].strip() == "it is sunny" : antecedent = "it is sunny"
	elif splitted[0].strip() == "it is rainy" : antecedent = "it is rainy"
	else: return None

	if antecedent not in antecedentCounter.keys(): antecedentCounter[antecedent] = 0
	antecedentCounter[antecedent] += 1

	consequentIndex = 1
	if "between" in antecedent:
		antecedent = antecedent + " " + splitted[1].replace(" ", "") + " and " + splitted[2].replace(" ", "")
		consequentIndex = 3

	consequent = ""
	if splitted[consequentIndex].strip() == "turn on the light": consequent = "turn on the room light"
	elif splitted[consequentIndex].strip() == "turn off the light": consequent = "turn off the room light"
	elif splitted[consequentIndex].strip() == "turn on the heating": consequent = "turn on the heating"
	elif splitted[consequentIndex].strip() == "turn off the heating": consequent = "turn off the heating"
	elif splitted[consequentIndex].strip() == "turn air conditioning on": consequent = "turn on the air conditioning"
	elif splitted[consequentIndex].strip() == "turn air conditioning off": consequent = "turn off the air conditioning"
	elif splitted[consequentIndex].strip() == "open the window": consequent = "open the windows"
	elif splitted[consequentIndex].strip() == "close the window": consequent = "close the windows"
	elif splitted[consequentIndex].strip() == "open curtains": consequent = "open the curtains"
	elif splitted[consequentIndex].strip() == "close curtains": consequent = "close the curtains"
	elif splitted[consequentIndex].strip() == "turn on the coffee machine": consequent = "turn on the coffee machine"
	elif splitted[consequentIndex].strip() == "turn off the coffee machine": consequent = "turn off the coffee machine"
	elif splitted[consequentIndex].strip() == "turn on the microwave": consequent = "turn on the microwave"
	elif splitted[consequentIndex].strip() == "turn off the microwave": consequent = "turn off the microwave"
	else: return None

	if consequent not in consequentCounter.keys(): consequentCounter[consequent] = 0
	consequentCounter[consequent] += 1
              
	ruleBody = "if " + antecedent + " then " + consequent

	return ruleBody

def login():
	
	global brules_username
	global brules_userUuid
	global brules_password
	global brules_sessionKey

	response = rest.request("/api/users/<username>/login", {'username' : brules_username, 'password' : brules_password})
	brules_sessionKey = response["sessionKey"]
	brules_userUuid = response["userUuid"]

	if response['request-error']: logerror(response)

def logout():

	global brules_username
	response = rest.request("/api/users/<username>/logout", {'username' : brules_username})

	if response['request-error']: logerror(response)


def deleteRule(ruleId):

	global brules_username
	global brules_buildingName
	global brules_userUuid
	global brules_sessionKey
	global brules_roomName


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete", {
			'username' : brules_username,
			'buildingName' : brules_buildingName,
			'roomName' : brules_roomName,
			'ruleId' : ruleId,
			'sessionKey' : brules_sessionKey, 
			'userUuid' : brules_userUuid
			})

	if response['request-error']: logerror(response)


def cleanRoom():

	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules", 
			{
			'username' : brules_username,
			'buildingName' : brules_buildingName,
			'roomName' : brules_roomName,
			'sessionKey' : brules_sessionKey, 
			'userUuid' : brules_userUuid,
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : False,
			'categoriesFilter' : None
			})

	if response['request-error']: logerror(response)

	for rule in response["rules"]:
		deleteRule(rule["id"])


def storeAndCheckRule(ruleBody, priority):

	global brules_username
	global brules_buildingName
	global brules_userUuid
	global brules_sessionKey
	global brules_roomName

	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/add", {
			'username' : brules_username,
			'buildingName' : brules_buildingName,
			'roomName' : brules_roomName,
			'priority' : priority, 
			'ruleBody' : ruleBody, 
			'sessionKey' : brules_sessionKey, 
			'userUuid' : brules_userUuid
			})

	if response['request-error']: logerror(response)

	return response





##### MAIN STARTS HERE #########################################################

backupResults()
login()
cleanRoom()

inputFileName = sys.argv[1]

f = open(inputFileName)
lines = f.readlines()
f.close()

rules = []
totalValidRules = 0
totalValidRuleSet = 0
totalInvalidRules = 0
totalInvalidRuleSet = 0

currentRuleset = {}
currentRuleset["rules"] = []

print "Translating the survey file..."

for line in lines:

	if "/" in line and ":" in line:
		currentRuleset["timestamp"] = line.split(",")[0].strip()

	if line.startswith("Rule_"):
		tRule = translateRule(line)
		if tRule : 

			if "the day is between" in tRule:
				antValues = tRule.split("then")[0].strip().replace("if the day is between", "")
				cons = tRule.split("then")[1].strip()
				
				day1 = antValues.split("and")[0].strip()
				day2 = antValues.split("and")[1].strip()

				if translateDay(day1) > translateDay(day2):
					tRule1 = "if the day is between " + day1 + " and Sunday then " + cons
					tRule2 = "if the day is between Monday and " + day2 + " then " + cons
					currentRuleset["rules"].append(tRule1)
					currentRuleset["rules"].append(tRule2)
					totalValidRules += 2
				else:
					currentRuleset["rules"].append(tRule)
					totalValidRules += 1

			else:

				currentRuleset["rules"].append(tRule)
				totalValidRules += 1

		else:
			totalInvalidRules += 1 
		

	if line.startswith('"'):
		if currentRuleset["rules"]:
			rules.append(copy.deepcopy(currentRuleset))
			totalValidRuleSet += 1
		else:
			totalInvalidRuleSet += 1
		currentRuleset["rules"] = []


print "DONE."

statsResults = {}

statsResults["totalValidRules"] = totalValidRules
statsResults["totalValidRuleSet"] = totalValidRuleSet
statsResults["totalInvalidRules"] = totalInvalidRules
statsResults["totalInvalidRuleSet"] = totalInvalidRuleSet
statsResults["antecedentStats"] = antecedentCounter
statsResults["consequentStats"] = consequentCounter

print statsResults

saveResults(str(json.dumps(statsResults, separators=(',',':'))))

print "Generating the room permutations..."

#maxElements = totalValidRuleSet
maxElements = 6		# maximum number of room occupants

roomList = []
roomListTokens = []

for setSize in range(0, maxElements):

	for i in range(0, maxElements):

		for iBody in range(i+setSize, maxElements):	

			currentSet = set()


			for iHead in range(i,i+setSize):
				currentSet.add(iHead)

			currentSet.add(iBody)

			token = "ID_" + str(list(currentSet))
			if token not in roomListTokens:
				roomList.append(copy.copy(currentSet))
				roomListTokens.append(token)



ruleCheckingResults = []
roomName = -1


for room in roomList[::-1]:

	roomName += 1
	roomRuleSet = []

	for userUuid in room:
		for rule in rules[userUuid]["rules"]:
			roomRuleSet.append(rule)

	logicalConflicts = 0
	runtimeConflicts = 0

	progress = -1
	progressTotal = math.factorial(len(roomRuleSet))

	for x in range(0, len(roomRuleSet)):
		for y in range(0, len(roomRuleSet)):

			if x > y:
				rule1 = roomRuleSet[x]
				rule2 = roomRuleSet[y]

				progress += 1

				if rule1 != rule2:
					
					statusText = str(roomName) +  "/" + str(len(roomList)) + "[u@" + str(len(room)) + "]" + "[r@" + str(len(roomRuleSet)) + "]" + "[%" + str(progress) + "/" + str(progressTotal) + "]" + " - "

					print statusText + "Testing conflict between '" + rule1 + "' VS '" + rule2 + "'"

					response1 = storeAndCheckRule(rule1, 1)
					response2 = storeAndCheckRule(rule2, 2)

					if response2['request-error']:
						if response2['request-errorName'] == "RuleValidationError":
							logicalConflicts += 1
							print  statusText + "[logicalConflicts] = " + str(logicalConflicts)
							logerror(statusText +  "LOGICALLY CONFLICTING RULES '" + rule1 + "' VS '" + rule2 + "'")
							logerror("[logicalConflicts] = " + str(logicalConflicts))

					elif response2['request-success']:
						if response1['category'] == response2['category']:
							runtimeConflicts += 1
							print statusText + "[runtimeConflicts] = " + str(runtimeConflicts)
							logerror(statusText +  "RUNTIME CONFLICTING RULES '" + rule1 + "' VS '" + rule2 + "'")
							logerror("[runtimeConflicts] = " + str(runtimeConflicts))

					if "id" in response1.keys(): deleteRule(response1["id"])
					if "id" in response2.keys(): deleteRule(response2["id"])

				

	currentResults = {}
	currentResults["roomName"] = roomName
	currentResults["room"] = room
	currentResults["occupants"] = len(room)
	currentResults["logicalConflicts"] = logicalConflicts
	currentResults["runtimeConflicts"] = runtimeConflicts

	ruleCheckingResults.append(currentResults)

	saveResults(currentResults)

logout()


print ruleCheckingResults
		