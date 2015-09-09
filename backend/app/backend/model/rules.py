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


class Rules:
	def __init__(self):
		pass

	def getActiveRulesId(self, buildingName = None, roomName = None):


		query = "SELECT * FROM active_rules"

		if buildingName and not roomName: query += " WHERE building_name = '@@building_name@@'"
		if buildingName and roomName: query += " WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@'"
		query += ";"
		
		if buildingName: query = query.replace("@@building_name@@", buildingName)
		if roomName: query = query.replace("@@room_name@@", roomName)
		

		database = Database()
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		rulesId = []
		for record in queryResult:
			ruleId = record[2]

			rulesId.append(ruleId)
		
		return rulesId

	def setActiveRule(self, buildingName, roomName, ruleId):



		if not (buildingName and roomName and ruleId):
			MissingInputDataError("Impossible to set an active rule without buildingName roomName or ruleId")

		query = "INSERT INTO `active_rules` (`building_name`, `room_name`, `rule_id`) VALUES ('@@building_name@@', '@@room_name@@', @@rule_id@@);"
		query = query.replace("@@building_name@@", buildingName)
		query = query.replace("@@room_name@@", roomName)
		query = query.replace("@@rule_id@@", str(ruleId))


		database = Database()
		database.open()
		database.executeWriteQuery(query)
		database.close()


	def resetActiveRules(self):

		database = Database()
		database.open()
		database.executeWriteQuery("TRUNCATE TABLE active_rules;")
		database.close()


		

	def __str__(self):
		return "Rules: "