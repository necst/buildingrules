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
from app.backend.model.action import Action

class Actions:
	def __init__(self):
		pass

	def getAllActions(self):

		actionList = []

		database = Database()
		database.open()
		query = "SELECT * FROM actions;"
		queryResult = database.executeReadQuery(query)

		for record in queryResult:
			actionId = record[0]
			category = record[1]
			actionName = record[2]
			ruleConsequent = record[3]
			description = record[4]

			action = Action(id = actionId, category = category, actionName = actionName, ruleConsequent = ruleConsequent, description = description)
			actionList.append(action)

		database.close()		

		return actionList

	def translateTemplate(self, language, actionTemplate):

		database = Database()
		database.open()
		query = "SELECT * FROM rule_translation_dictionary WHERE language = '@@language@@' AND original = '@@actionTemplate@@';"
		query = query.replace('@@language@@', language)
		query = query.replace('@@actionTemplate@@', actionTemplate)
		queryResult = database.executeReadQuery(query)
		database.close()

		if len(queryResult) > 0:
			translation = queryResult[0][3]
			return translation
				
		raise RuleTranslationNotFoundError("Impossibile to translate " + actionTemplate)

	def __str__(self):
		return "Actions: "