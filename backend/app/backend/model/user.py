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
import json
import datetime
from app.backend.commons.errors import *
from app.backend.commons.database import Database



class User:
	def __init__(self, uuid = None, username = None, email = None, password = None, personName = None, level = None, registrationTimestamp = None):
		
		self.uuid = uuid
		self.username = username
		self.email = email
		self.password = password
		self.personName = personName
		self.level = level
		self.registrationTimestamp = registrationTimestamp

	def getMaxRoomPriority(self):
		if self.level:
			return int(self.level)

		raise ClassNotInitializedError("Missing input data")

	def getMaxGroupPriority(self):
		if self.level:
			return int(self.level)

		raise ClassNotInitializedError("Missing input data")


	def getRooms(self):

		from app.backend.model.room import Room

		database = Database()
		database.open()

		query = "SELECT * FROM users_rooms WHERE user_uuid = '@@uuid@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for record in queryResult:
			roomName = record[0]
			buildingName = record[1]

			room = Room(roomName = roomName,  buildingName = buildingName)
			room.retrieve()

			roomList.append(room)

		return roomList

	def getBuildings(self):		
		
		buildingList = []
		buildingNameList = []
		for room in self.getRooms():
			currentBuilding = room.getBuilding()
			if currentBuilding.buildingName not in buildingNameList:
				buildingList.append(currentBuilding)
				buildingNameList.append(currentBuilding.buildingName)

		return buildingList

	def getGroups(self):
		
		groupList = []
		groupIdList = []

		for room in self.getRooms():
			roomGroupList = room.getGroups()

			for group in roomGroupList:
				if group.id not in groupIdList:
					groupIdList.append(group.id)
					groupList.append(group)

		return groupList


	def getCreatedRules(self, includeDisabled = False, includeDeleted = False):

		from app.backend.model.rule import Rule


		query = "SELECT id FROM rules WHERE author_uuid = '@@uuid@@'"
		query += " AND enabled='1'" if not includeDisabled else ""
		query += " AND deleted='0'" if not includeDeleted else ""
		query += ";"


		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		ruleList = []
		for record in queryResult:
			ruleId = record[0]

			rule = Rule(id = ruleId)
			rule.retrieve()

			ruleList.append(rule)

		return ruleList


	def addRule(self, rule):
		rule.authorUuid = self.uuid
		rule.store()

	def deleteRule(self, rule):
		rule.delete()			

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.uuid 					!= None	: queryTemplate = queryTemplate.replace("@@uuid@@", str(self.uuid))
		if self.username				!= None	: queryTemplate = queryTemplate.replace("@@username@@", self.username)
		if self.email					!= None	: queryTemplate = queryTemplate.replace("@@email@@", self.email)
		if self.password				!= None	: queryTemplate = queryTemplate.replace("@@password@@", self.password)
		if self.personName 				!= None	: queryTemplate = queryTemplate.replace("@@person_name@@", self.personName)
		if self.level					!= None	: queryTemplate = queryTemplate.replace("@@level@@", str(self.level))
		if self.registrationTimestamp	!= None	: queryTemplate = queryTemplate.replace("@@registration_timestamp@@", self.registrationTimestamp.strftime('%Y-%m-%d %H:%M:%S'))

		return queryTemplate


	def store(self):

		if not self.registrationTimestamp:
			self.registrationTimestamp = datetime.datetime.now() 

		database = Database()
		database.open()

		query = "SELECT COUNT(uuid) FROM users WHERE uuid = '@@uuid@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE users SET username = '@@username@@', email = '@@email@@', password = '@@password@@', person_name = '@@person_name@@', level = '@@level@@', registration_timestamp = '@@registration_timestamp@@' WHERE uuid = '@@uuid@@';"
		else:
			query = "INSERT INTO users (username, email, password, person_name, level, registration_timestamp) VALUES ('@@username@@','@@email@@', '@@password@@', '@@person_name@@', '@@level@@', '@@registration_timestamp@@');"
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		self.uuid = int(database.getLastInsertedId()) if not self.uuid else self.uuid
		database.close()


	def retrieve(self):

		if not self.uuid:
			if self.username and not self.password:
				query = "SELECT * FROM users WHERE username = '@@username@@';"
			elif self.username and self.password:
				query = "SELECT * FROM users WHERE username = '@@username@@' AND password = '@@password@@';"
			else:
				raise ClassNotInitializedError("Impossibile querying a user: missing input data")
		else:
			query = "SELECT * FROM users WHERE uuid = '@@uuid@@';"


		database = Database()
		database.open()

		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if len(queryResult) > 0:
			self.uuid = int(queryResult[0][0])
			self.username = queryResult[0][1]
			self.email = queryResult[0][2]
			self.password = queryResult[0][3]
			self.personName = queryResult[0][4]
			self.level = int(queryResult[0][5])
			self.registrationTimestamp = queryResult[0][6]

		else:
			database.close()
			raise UserNotFoundError("Impossibile to find any user with the provided values")

		database.close()



	def delete(self):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed into table users_rooms"

		database = Database()
		database.open()

		query = "DELETE FROM users WHERE uuid = '@@uuid@@'"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		response = {}

		response["uuid"] = self.uuid
		response["username"] = self.username
		response["email"] = self.email
		response["personName"] = self.personName
		response["level"] = self.level
		response["registrationTimestamp"] = self.registrationTimestamp.strftime('%Y-%m-%d %H:%M:%S') if self.registrationTimestamp else None
		response["maxRoomPriority"] = self.getMaxRoomPriority()
		response["maxGroupPriority"] = self.getMaxGroupPriority()

		return response

	def __str__(self):
		return "User " + str(json.dumps(self.getDict(), separators=(',',':')))

