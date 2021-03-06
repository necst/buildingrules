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

import rest
import sys

def getRoomCategory(roomName):
	
	if roomName == 2107:	return "KITCHEN"
	if roomName == 2144:	return "STORAGE"
	if roomName == 3208:	return "CONFERENCE"
	if roomName == 3208:	return "LOBBY"
	if roomName == 2140:	return "MEETING"
	if roomName == 2154:	return "MEETING"
	if roomName == 3113:	return "LABORATORY"
	
	return "OFFICE"


username = "admin"
password = "brulesAdmin2014"
buildingName = "CSE"

rulesToAdd = []
rulesToAdd.append({'priority' : 0,  'ruleBody' : "if no rule specified then turn off the room light", 'roomCategory' : ["ALL"]})
rulesToAdd.append({'priority' : 1,  'ruleBody' : "if time is between 17.00 and 20.00 then turn on the room light", 'roomCategory' : ["ALL"]})
rulesToAdd.append({'priority' : 2,  'ruleBody' : "if today is Sunday then turn off the room light", 'roomCategory' : ["ALL"]})
rulesToAdd.append({'priority' : 0,  'ruleBody' : "if no rule specified then set temperature between 65F and 79F", 'roomCategory' : ["ALL"]})
rulesToAdd.append({'priority' : 0,  'ruleBody' : "if no rule specified then set humidity between 44% and 58%", 'roomCategory' : ["ALL"]})
rulesToAdd.append({'priority' : 0,  'ruleBody' : "if no rule specified then turn on the exhaust fan", 'roomCategory' : ["KITCHEN"]})

# login ##########################################
response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})
sessionKey = response["sessionKey"]
userUuid = response["userUuid"]


# getting room list ##########################################
response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {
			'username' : username,
			'buildingName' : buildingName,
			'sessionKey' : sessionKey,
			'userUuid' : userUuid
			})

roomList = response["rooms"]


# adding the rules ##########################################
for room in roomList:
	roomName = room["roomName"]
	roomCategory = getRoomCategory(int(roomName))
	
	for rule in rulesToAdd:

		addRule = False
		if (rule['roomCategory'][0] == "ALL") or (roomCategory in rule['roomCategory']):
			
			response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/add", {
						'username' : username,
						'buildingName' : buildingName,
						'roomName' : roomName,
						'priority' : rule['priority'], 
						'ruleBody' : rule['ruleBody'], 
						'sessionKey' : sessionKey, 
						'userUuid' : userUuid
						})
			
			if response['request-success']:
				print "[   OK   ] " + rule['ruleBody']
			else:
				print "[ FAILED ]  " + rule['ruleBody'] +  " - " + response["request-errorName"]
			print response

response = rest.request("/api/users/<username>/logout", {'username' : username})
sys.exit()

