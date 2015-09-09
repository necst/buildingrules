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
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Building:
	def __init__(self, buildingName = None, label = None, description = None):

			self.buildingName = buildingName
			self.label = label
			self.description = description

	def getBuilding(self):
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : non yet implemented"

	def getRooms(self):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : non yet tested"

		from app.backend.model.room import Room
		
		query = "SELECT room_name FROM rooms WHERE building_name = '@@building_name@@';"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for roomRecord in queryResult:
			room = Room(roomName = roomRecord[0], buildingName = self.buildingName)
			room.retrieve()
			roomList.append(room)

		return roomList

	def getUnassignedRooms(self):

		from app.backend.model.room import Room
		
		query = "SELECT * FROM rooms where (room_name,building_name) NOT IN (SELECT room_name,building_name FROM users_rooms) AND building_name='@@building_name@@'"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for roomRecord in queryResult:
			room = Room(roomName = roomRecord[0], buildingName = self.buildingName)
			room.retrieve()
			roomList.append(room)

		return roomList


	def getGroups(self):
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : non yet tested"

		from app.backend.model.group import Group
		
		query = "SELECT id FROM groups WHERE building_name = '@@building_name@@';"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		groupList = []
		for groupRecord in queryResult:
			group = Group(id = groupRecord[0], buildingName = self.buildingName)
			group.retrieve()
			groupList.append(group)

		return groupList

	def getCrossRoomValidationGroups(self, roomName = None, validationCategories = None):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : non yet tested"

		from app.backend.model.group import Group
		
		query = "SELECT id FROM groups WHERE building_name = '@@building_name@@' AND cross_rooms_validation = '1';"

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		groupList = []
		for groupRecord in queryResult:
			group = Group(id = groupRecord[0], buildingName = self.buildingName)
			group.retrieve()

			if validationCategories:
				queriedValidationCategories = set(validationCategories)
				groupValidationCategories = set(group.crossRoomsValidationCategories)

				if queriedValidationCategories.issubset(groupValidationCategories):
					groupList.append(group)	

			else:
				groupList.append(group)

		if not roomName and not validationCategories:
			return groupList

		
		if roomName:
			filteredGroupList = []
			for group in groupList:

				for room in group.getRooms():
					if room.roomName == roomName:
						filteredGroupList.append(group)

			return filteredGroupList

		raise UnknownError()

	def getRules(self, includeDisabled = False, includeDeleted = False):		
		

		from app.backend.model.rule import Rule
		
		query = "SELECT * FROM rules WHERE building_name = '@@building_name@@'"
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
			priority = int(record[1])
			category = record[2]
			buildingName = record[3]
			authorUuid = int(record[6])
			antecedent = record[7]
			consequent = record[8]
			enabled = bool(int(record[9]))
			deleted = bool(int(record[10]))
			creationTimestamp = record[11]
			lastEditTimestamp = record[12]

			groupId = int(record[4])
			roomName = record[5]

			groupId = groupId if groupId != -1 else None
			roomName = roomName if roomName != "None" else None

			rule = Rule(id = ruleId, priority = priority, category = category, buildingName = buildingName, groupId = groupId, roomName = roomName, authorUuid = authorUuid, 
				antecedent = antecedent, consequent = consequent, enabled = enabled, deleted = deleted, creationTimestamp = creationTimestamp, lastEditTimestamp = lastEditTimestamp)

	
			ruleList.append(rule)

		return ruleList


	def addRoom(self, room):
		room.buildingName = self.buildingName
		room.store()
		return room

	def addGroup(self, group):
		group.buildingName = self.buildingName
		group.store()
		return group

	def deleteRoom(self, room):
		room.delete()

	def deleteGroup(self, group):
		group.delete()

	def checkUserBinding(self, user):

		database = Database()

		query = "SELECT user_uuid FROM users_rooms WHERE building_name = '@@building_name@@' and user_uuid = '@@user_uuid@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace('@@user_uuid@@', str(user.uuid))
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		if len(queryResult) == 0:
			raise UserBuildingBindingError("The user is not associated with the requested building")


	def __replaceSqlQueryToken(self, queryTemplate):
		if self.buildingName 	!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.label			!= None	: 	queryTemplate = queryTemplate.replace("@@label@@", self.label)
		if self.description 	!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):
		database = Database()
		database.open()

		query = "SELECT COUNT(building_name) FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE buildings SET label = '@@label@@', description = '@@description@@' WHERE building_name = '@@building_name@@';"
		else:
			query = "INSERT INTO buildings (building_name, label, description) VALUES ('@@building_name@@', '@@label@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):
		database = Database()
		database.open()

		query = "SELECT * FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.buildingName = queryResult[0][0]
			self.label = queryResult[0][1]
			self.description = queryResult[0][2]
		else:
			database.close()
			raise BuildingNotFoundError("Impossibile to find any building with the provided values")

		database.close()


	def delete(self):
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - class Building"

		database = Database()
		database.open()

		query = "DELETE FROM buildings WHERE building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()


	def getDict(self):
		
		response = {}

		response["buildingName"] = self.buildingName
		response["label"] = self.label
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Building " + str(json.dumps(self.getDict(), separators=(',',':')))