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

class RulePriority:
	def __init__(self, buildingName = None, roomName = None, ruleId = None, rulePriority = None):

			self.buildingName = buildingName
			self.roomName = roomName
			self.ruleId = ruleId
			self.rulePriority = rulePriority

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.buildingName 	!= None	: 	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.roomName 		!= None	: 	queryTemplate = queryTemplate.replace("@@room_name@@", self.roomName)
		if self.ruleId			!= None	: 	queryTemplate = queryTemplate.replace("@@rule_id@@", str(self.ruleId))
		if self.rulePriority	!= None	: 	queryTemplate = queryTemplate.replace("@@rule_priority@@", str(self.rulePriority))

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(building_name) FROM rules_priority WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@' AND rule_id = '@@rule_id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE rules_priority SET rule_priority = '@@rule_priority@@' WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@' AND rule_id = '@@rule_id@@';"
		else:
			query = "INSERT INTO rules_priority (building_name, room_name, rule_id, rule_priority) VALUES ('@@building_name@@', '@@room_name@@', '@@rule_id@@', '@@rule_priority@@');"	
	


		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if not (self.buildingName and self.roomName and self.ruleId): raise MissingInputDataError("Missing input to get a rule priority")

		database = Database()
		database.open()

		query = "SELECT * FROM rules_priority WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@' AND rule_id = '@@rule_id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.rulePriority = queryResult[0][3]
		else:
			database.close()
			raise RoomRulePriorityNotFoundError("Impossibile to find the requested rule priority record")

		database.close()


	def delete(self):

		if not (self.buildingName and self.roomName and self.ruleId): raise MissingInputDataError("Missing input to get a rule priority")
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - RulePriority class"

		database = Database()
		database.open()

		query = "DELETE FROM rules_priority WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@' AND rule_id = '@@rule_id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["buildingName"] = self.buildingName
		response["roomName"] = self.roomName
		response["ruleId"] = self.ruleId
		response["rulePriority"] = self.rulePriority

		return response	

	def __str__(self):
		return "RulePriority " + str(json.dumps(self.getDict(), separators=(',',':')))