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

class Group:
	def __init__(self, id = None, buildingName = None, description = None, crossRoomsValidation = None, crossRoomsValidationCategories = None):

			self.id = id
			self.buildingName = buildingName
			self.description = description
			self.crossRoomsValidation = crossRoomsValidation
			self.crossRoomsValidationCategories = crossRoomsValidationCategories

	def getBuilding(self):
		from app.backend.model.building import Building

		building = Building(buildingName = self.buildingName)
		building.retrieve()
		return building


	def getRooms(self):
		
		from app.backend.model.room import Room

		database = Database()
		database.open()

		query = "SELECT * FROM rooms_groups WHERE group_id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		roomList = []
		for record in queryResult:
			buildingName = record[1]
			roomName = record[2]
			
			room = Room(roomName = roomName,  buildingName = buildingName)
			room.retrieve()

			roomList.append(room)

		return roomList


	def getRules(self, excludedRuleId = False, includeDisabled = False, includeDeleted = False, categoriesFilter = None):		

		from app.backend.model.rule import Rule

		query = "SELECT id FROM rules WHERE group_id = '@@id@@' @@__EXCLUDED_RULE_ID__@@"
		query += " AND enabled='1'" if not includeDisabled else ""
		query += " AND deleted='0'" if not includeDeleted else ""

		if categoriesFilter:
			query += " AND (@@__CATEGORY_FILTERS__@@)"
			categoryFilterQuery = ""

			for category in json.loads(categoriesFilter):
				categoryFilterQuery += "category = '" + category + "' OR "

			query = query.replace("@@__CATEGORY_FILTERS__@@", categoryFilterQuery)
			query = query.replace(" OR )", ")")

		query += ";"


		if excludedRuleId:
			query = query.replace("@@__EXCLUDED_RULE_ID__@@", "AND NOT id = " + str(excludedRuleId))
		else:
			query = query.replace("@@__EXCLUDED_RULE_ID__@@", "")


		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)
		database.close()

		
		ruleList = []
		for ruleRecord in queryResult:
			rule = Rule(ruleRecord[0])
			rule.retrieve()
			ruleList.append(rule)

		return ruleList


	def addRule(self, rule):

		rule.groupId = self.id
		rule.buildingName = self.buildingName
		rule.store()

		return rule


	def addRoom(self, room):
		database = Database()
		database.open()

		query = "INSERT INTO rooms_groups (group_id, building_name, room_name) VALUES ('@@id@@', '@@building_name@@', '@@room_name@@');"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@room_name@@", str(room.roomName))
		database.executeWriteQuery(query)

		database.close()


	def deleteRoom(self, room):
		database = Database()
		database.open()

		query = "DELETE FROM rooms_groups WHERE room_name = '@@room_name@@' AND building_name = '@@building_name@@' AND group_id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		query = query.replace("@@room_name@@", str(room.roomName))
		database.executeWriteQuery(query)

		database.close()

	def deleteRule(self, rule):
		rule.delete()

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 								!= None	:	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.buildingName 					!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.description 					!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)
		if self.crossRoomsValidation 			!= None	: 	queryTemplate = queryTemplate.replace("@@cross_rooms_validation@@", str(int(self.crossRoomsValidation)))
		if self.crossRoomsValidationCategories 	!= None	: 	queryTemplate = queryTemplate.replace("@@cross_rooms_validation_categories@@", json.dumps(self.crossRoomsValidationCategories, separators=(',',':')))

		return queryTemplate

	def store(self):


		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE groups SET description = '@@description@@', cross_rooms_validation = '@@cross_rooms_validation@@', cross_rooms_validation_categories = '@@cross_rooms_validation_categories@@' WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		else:
			query = "INSERT INTO groups (building_name, description, cross_rooms_validation, cross_rooms_validation_categories) VALUES ('@@building_name@@', '@@description@@', '@@cross_rooms_validation@@', '@@cross_rooms_validation_categories@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		self.id = int(database.getLastInsertedId()) if not self.id else self.id
		database.close()



	def retrieve(self):

		if not(self.id and self.buildingName):
			raise Exception("Group querying required both group id and buildingName")

		database = Database()
		database.open()

		query = "SELECT * FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if len(queryResult) > 0:
			self.id = int(queryResult[0][0])
			self.buildingName = queryResult[0][1]
			self.description = queryResult[0][2]
			self.crossRoomsValidation = bool(int(queryResult[0][3]))
			self.crossRoomsValidationCategories = json.loads(queryResult[0][4])
		else:
			database.close()
			raise Exception("Impossibile to find any group with the provided values")

		database.close()


	def delete(self):
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - Group class"

		database = Database()
		database.open()

		query = "DELETE FROM groups WHERE id = '@@id@@' AND building_name = '@@building_name@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["buildingName"] = self.buildingName
		response["description"] = self.description
		response["crossRoomsValidation"] = self.crossRoomsValidation
		response["crossRoomsValidationCategories"] = self.crossRoomsValidationCategories 

		return response	


	def __str__(self):
		return "Group " + str(json.dumps(self.getDict(), separators=(',',':')))