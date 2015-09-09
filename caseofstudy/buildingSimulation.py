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

# login ##########################################
response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})
sessionKey = response["sessionKey"]
userUuid = response["userUuid"]


# starting simulation ##########################################
response = rest.request("/api/test", {
			'username' : username,
			'buildingName' : buildingName,
			'sessionKey' : sessionKey,
			'userUuid' : userUuid
			})

roomList = response["rooms"]

response = rest.request("/api/users/<username>/logout", {'username' : username})
sys.exit()

