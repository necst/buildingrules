############################################################
#
# BuildingRules Project 
# Politecnico di Milano
# Author: Alessandro A. Nacci
#
# This code is confidential
# Milan, March 2014
#
############################################################

import sys
import os
import sys
import subprocess
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from database import Database
import rest
import math

sessionKey = None
userUuid = None
username = "admin"
password = "brulesAdmin2014"




def dictToCsv(dictionary, fileName, description):

	if not fileName.endswith(".csv"): fileName += ".csv"
	if not fileName.startswith("results/"): fileName = "results/" + fileName

	if not os.path.exists("results/"): os.makedirs("results/")

	out_file = open(fileName,"w")
	
	for k,v in dictionary.iteritems():
		out_file.write(str(k) + ";" + str(v) + ";" + "\n")	

	
	out_file.write("\n\n\n")
	out_file.write(description)

	out_file.close()



def execProcess(cmd):

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()

	return output


def getUserActionOnRule(action):
	currentFile = "../../frontend/logs/api_requests.log"
	cmd = "cat " + currentFile + " | grep rules | grep " + action + " | grep -c API_REQUEST"
	output = execProcess(cmd).replace("\n","").strip()
	return {action : output}


def getUserActionOnRulePerDay(action):

	result = {}

	for day in getExperimentDaysList():
		currentFile = "../../frontend/logs/api_requests.log"
		cmd = "cat " + currentFile + ' | grep rules | grep ' + action + ' | grep API_REQUEST | grep -c "> ' + day + '"'
		output = execProcess(cmd).replace("\n","").strip()
		result.update({ day : output })

	return result


def getExperimentDaysList():
	daysList = []

	firstDay = date(2014,02,1)
	today = date.today()
	deltaDays = (today - firstDay).days

	currentDay = firstDay
	for i in range(1, deltaDays+2):
		daysList.append(currentDay.strftime("%Y-%m-%d"))
		currentDay += timedelta(days=1)

	return daysList


def getRoomList():

	query = "SELECT DISTINCT room_name FROM `rooms`"

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()

	roomList = []
	
	for record in queryResult:
		roomList.append(record[0])

	return roomList

def getRuleList(roomName = None):

	query = "SELECT * FROM `rules`"
	if roomName: 
		query = "SELECT * FROM `rules` WHERE room_name = '" + roomName +"'"

	print query

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()


	ruleList = []
	
	for record in queryResult:
		recDict = {}
		recDict["id"] = record[0]
		recDict["priority"] = record[1]
		recDict["category"] = record[2]
		recDict["buildingName"] = record[3]
		recDict["groupId"] = record[4]
		recDict["roomName"] = record[5]
		recDict["authorUuid"] = record[6]
		recDict["antecedent"] = record[7]
		recDict["consequent"] = record[8]
		recDict["enabled"] = record[9]
		recDict["deleted"] = record[10]
		recDict["creationTimestamp"] = record[11] 
		recDict["lastEditTimestamp"] = record[12]

		ruleList.append(recDict)

	return ruleList


def getTimeConflictData(recordFilter):

	if recordFilter == "ALL":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification%'"
	elif recordFilter == "SUCCESS":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification [SUCCESS]%'"
	elif recordFilter == "FAILED":
		query = "SELECT * FROM `logs` WHERE `logMessage` LIKE '%RoomRuleVerification [FAILED]%'"
	else:
		print "error filter"
		sys.exit()

	database = Database()
	database.open()
	queryResult = database.executeReadQuery(query)
	database.close()


	ruleVerificationStats_cardinality = {}
	ruleVerificationStats_avg = {}
	ruleVerificationStats_stdev = {}
	ruleVerificationStats_sum = {}
	ruleVerificationStats_squareSum = {}
	ruleVerificationStats_max = {}
	ruleVerificationStats_min = {}

	for record in queryResult:
		
		numberOfRulesStrIndex = record[2].find("#rules=") + len("#rules=")
		numberOfRules = record[2][numberOfRulesStrIndex:].split("-")[0].strip()

		millisecondsStrIndex = record[2].find("opTimeMilliseconds:") + len("opTimeMilliseconds:")
		milliseconds = record[2][millisecondsStrIndex:].strip()

		numberOfRules = int(numberOfRules)
		milliseconds = int(milliseconds)

		if numberOfRules not in ruleVerificationStats_cardinality.keys(): ruleVerificationStats_cardinality[numberOfRules] = 0
		ruleVerificationStats_cardinality[numberOfRules] += 1

		if numberOfRules not in ruleVerificationStats_sum.keys(): ruleVerificationStats_sum[numberOfRules] = 0
		if numberOfRules not in ruleVerificationStats_squareSum.keys(): ruleVerificationStats_squareSum[numberOfRules] = 0
		ruleVerificationStats_sum[numberOfRules] += milliseconds
		ruleVerificationStats_squareSum[numberOfRules] += (milliseconds * milliseconds)

		if numberOfRules not in ruleVerificationStats_max.keys(): ruleVerificationStats_max[numberOfRules] = 0
		if milliseconds > ruleVerificationStats_max[numberOfRules]: ruleVerificationStats_max[numberOfRules] = milliseconds
		
		if numberOfRules not in ruleVerificationStats_min.keys(): ruleVerificationStats_min[numberOfRules] = sys.maxint
		if milliseconds < ruleVerificationStats_min[numberOfRules]: ruleVerificationStats_min[numberOfRules] = milliseconds


	# Computing average
	for numberOfRules in ruleVerificationStats_cardinality.keys():
		ruleVerificationStats_avg[numberOfRules] = ruleVerificationStats_sum[numberOfRules] / ruleVerificationStats_cardinality[numberOfRules]
		mean = ruleVerificationStats_avg[numberOfRules]
		ruleVerificationStats_stdev[numberOfRules] = math.sqrt((ruleVerificationStats_squareSum[numberOfRules] / ruleVerificationStats_cardinality[numberOfRules]) - (mean * mean)) 

	return ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min, ruleVerificationStats_stdev


def getRuleAntecedentTriggerInfo(ruleAntecedent):
	global sessionKey
	global userUuid

	response = rest.request("/api/tools/triggers/translate", {
			'sessionKey' : sessionKey,
			'userUuid' : userUuid,
			'antecedent' : ruleAntecedent
			})

	return response["triggers"]


def getRuleConsequentActionInfo(ruleConsequent):
	global sessionKey
	global userUuid

	response = rest.request("/api/tools/actions/translate", {
			'sessionKey' : sessionKey,
			'userUuid' : userUuid,
			'consequent' : ruleConsequent
			})

	return response["action"]


def login():

	global sessionKey
	global userUuid
	global username
	global password

	response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})
	sessionKey = response["sessionKey"]
	userUuid = response["userUuid"]



def getRuleUsageFrequency(roomName = None):
	triggerCategoryCounter = {}
	triggerNameCounter = {}

	actionCategoryCounter = {}
	actionNameCounter = {}

	triggerActionCategoryCounter = {}
	triggerActionNameCounter = {}

	triggerCategories = set()
	triggerNames = set()
	actionCategories = set()
	actionNames = set()

	ruleList = getRuleList(roomName= roomName)

	for rule in ruleList:

		triggersInfo = getRuleAntecedentTriggerInfo(rule["antecedent"])
		actionInfo = getRuleConsequentActionInfo(rule["consequent"])

		actionCategory = actionInfo["category"]
		actionName = actionInfo["actionName"]

		actionCategories.add(actionCategory)
		actionNames.add(actionName)

		if actionCategory not in actionCategoryCounter.keys(): actionCategoryCounter[actionCategory] = 0
		if actionName not in actionNameCounter.keys(): actionNameCounter[actionName] = 0

		actionCategoryCounter[actionCategory] += 1
		actionNameCounter[actionName] += 1
		
		for triggerInfo in triggersInfo:

			trigger = triggerInfo["trigger"]

			triggerCategory = trigger["category"]
			triggerName = trigger["triggerName"]

			triggerCategories.add(triggerCategory)
			triggerNames.add(triggerName)

			if triggerCategory not in triggerCategoryCounter.keys(): triggerCategoryCounter[triggerCategory] = 0
			if triggerName not in triggerNameCounter.keys(): triggerNameCounter[triggerName] = 0

			triggerCategoryCounter[triggerCategory] += 1
			triggerNameCounter[triggerName] += 1

			if triggerCategory not in triggerActionCategoryCounter.keys(): triggerActionCategoryCounter[triggerCategory] = {}
			if triggerName not in triggerActionNameCounter.keys(): triggerActionNameCounter[triggerName] = {}

			if actionCategory not in triggerActionCategoryCounter[triggerCategory].keys() :  triggerActionCategoryCounter[triggerCategory][actionCategory] = 0
			if actionName not in triggerActionNameCounter[triggerName].keys() :  triggerActionNameCounter[triggerName][actionName] = 0

			triggerActionCategoryCounter[triggerCategory][actionCategory] += 1
			triggerActionNameCounter[triggerName][actionName] += 1


	if not os.path.exists("results/"): os.makedirs("results/")

	_CSV_SEP = ";"
	csvFileContent = ""

	csvFileContent += _CSV_SEP
	for action in sorted(list(actionNames)):
		csvFileContent += action + _CSV_SEP

	csvFileContent += "\n"
	for trigger in sorted(list(triggerNames)):
		csvFileContent += trigger + _CSV_SEP
		for action in sorted(list(actionNames)):
			try:
				csvFileContent += str(triggerActionNameCounter[trigger][action]) + _CSV_SEP
			except:
				csvFileContent += "0" + _CSV_SEP
		csvFileContent += "\n"

	#print csvFileContent 

	fileName = "results/triggerActionNameCounter_ruleNumber" + str(len(ruleList))
	if roomName: fileName = "results/triggerActionNameCounter_" + roomName + "_ruleNumber" + str(len(ruleList))

	fileName += ".csv"

	out_file = open(fileName,"w")
	out_file.write(csvFileContent)
	out_file.close()


	############################################################################################

	_CSV_SEP = ";"
	csvFileContent = ""

	csvFileContent += _CSV_SEP
	for action in sorted(list(actionCategories)):
		csvFileContent += action + _CSV_SEP

	csvFileContent += "\n"
	for trigger in sorted(list(triggerCategories)):
		csvFileContent += trigger + _CSV_SEP
		for action in sorted(list(actionCategories)):
			try:
				csvFileContent += str(triggerActionCategoryCounter[trigger][action]) + _CSV_SEP
			except:
				csvFileContent += "0" + _CSV_SEP
		csvFileContent += "\n"

	#print csvFileContent 

	fileName = "results/triggerActionCategoryCounter" + str(len(ruleList))
	if roomName: fileName = "results/triggerActionCategoryCounter_" + roomName + "_ruleNumber" + str(len(ruleList))
	fileName += ".csv"
	out_file = open(fileName,"w")
	out_file.write(csvFileContent)
	out_file.close()


###################################################################################################
###################################################################################################
###################################################################################################


login()

getRuleUsageFrequency()

for roomName in getRoomList():
	print "Reading for " + roomName + "..."
	getRuleUsageFrequency(roomName)

#GETTING DATA ABOUT THE CONFLICT DETECTION (BOTH SUCCESS AND FAIL)
ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min, ruleVerificationStats_stdev = getTimeConflictData("ALL")

dictToCsv(ruleVerificationStats_avg, "ruleVerificationStats_ALL_avg", "Average conflict detection time (ms)")
dictToCsv(ruleVerificationStats_max, "ruleVerificationStats_ALL_max", "Maximum conflict detection time (ms)")
dictToCsv(ruleVerificationStats_min, "ruleVerificationStats_ALL_min", "Minimum conflict detection time (ms)")
dictToCsv(ruleVerificationStats_stdev, "ruleVerificationStats_ALL_stdev", "Standard deviation conflict detection time")



ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min, ruleVerificationStats_stdev = getTimeConflictData("SUCCESS")

dictToCsv(ruleVerificationStats_avg, "ruleVerificationStats_SUCCESS_avg", "Average conflict detection time (ms) - Filtering only SUCCESS verifications")
dictToCsv(ruleVerificationStats_max, "ruleVerificationStats_SUCCESS_max", "Maximum conflict detection time (ms) - Filtering only SUCCESS verifications")
dictToCsv(ruleVerificationStats_min, "ruleVerificationStats_SUCCESS_min", "Minimum conflict detection time (ms) - Filtering only SUCCESS verifications")
dictToCsv(ruleVerificationStats_stdev, "ruleVerificationStats_SUCCESS_stdev", "Standard deviation conflict detection time - Filtering only SUCCESS verifications")



ruleVerificationStats_avg, ruleVerificationStats_max, ruleVerificationStats_min, ruleVerificationStats_stdev = getTimeConflictData("FAILED")

dictToCsv(ruleVerificationStats_avg, "ruleVerificationStats_FAILED_avg", "Average conflict detection time (ms) - Filtering only FAILED verifications")
dictToCsv(ruleVerificationStats_max, "ruleVerificationStats_FAILED_max", "Maximum conflict detection time (ms) - Filtering only FAILED verifications")
dictToCsv(ruleVerificationStats_min, "ruleVerificationStats_FAILED_min", "Minimum conflict detection time (ms) - Filtering only FAILED verifications")
dictToCsv(ruleVerificationStats_stdev, "ruleVerificationStats_FAILED_stdev", "Standard deviation conflict detection time - Filtering only FAILED verifications")



#GETTING DATA ABOUT THE USERS REQUEST (ADD EDIT RULE)
userActionRequests = {}
userActionRequests.update( getUserActionOnRule("add") )
userActionRequests.update( getUserActionOnRule("edit") )
userActionRequests.update( getUserActionOnRule("delete") )
userActionRequests.update( getUserActionOnRule("disable") )
userActionRequests.update( getUserActionOnRule("enable") )

dictToCsv(userActionRequests, "userActionRequests", "Number of requests on rules by the users")

dictToCsv( getUserActionOnRulePerDay("add"), "userActionRequests_perDay_ADD", "Number of ADD requests by the users per day")
dictToCsv( getUserActionOnRulePerDay("edit"), "userActionRequests_perDay_EDIT", "Number of EDIT requests by the users per day")
dictToCsv( getUserActionOnRulePerDay("delete"), "userActionRequests_perDay_DELETE", "Number of DELETE requests by the users per day")
dictToCsv( getUserActionOnRulePerDay("disable"), "userActionRequests_perDay_DISABLE", "Number of DISABLE requests by the users per day")
dictToCsv( getUserActionOnRulePerDay("enable"), "userActionRequests_perDay_ENABLE", "Number of ENABLE requests by the users per day")

