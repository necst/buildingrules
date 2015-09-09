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

class Action:
	def __init__(self, id = None, category = None, actionName = None, ruleConsequent = None, description = None):

			self.id = id
			self.category = category
			self.actionName = actionName
			self.ruleConsequent = ruleConsequent
			self.description = description

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.category 		!= None	: 	queryTemplate = queryTemplate.replace("@@category@@", self.category)
		if self.actionName 		!= None	: 	queryTemplate = queryTemplate.replace("@@action_name@@", self.actionName)
		if self.ruleConsequent	!= None	: 	queryTemplate = queryTemplate.replace("@@rule_consequent@@", self.ruleConsequent)
		if self.description		!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM actions WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE actions SET category = '@@category@@', action_name = '@@action_name@@', rule_consequent = '@@rule_consequent@@', description = '@@description@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO actions (category, action_name, rule_consequent, description) VALUES ('@@category@@', '@@action_name@@', '@@rule_consequent@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if self.id:
			query = "SELECT * FROM actions WHERE id = '@@id@@';"
		elif self.actionName:
			query = "SELECT * FROM actions WHERE action_name = '@@action_name@@';"
		else:
			raise MissingInputDataError("Impossibile to query any action with missing parameters")
			

		database = Database()
		database.open()

		
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.category = queryResult[0][1]
			self.actionName = queryResult[0][2]
			self.ruleConsequent = queryResult[0][3]
			self.description = queryResult[0][4]
		else:
			database.close()
			raise ActionNotFoundError("Impossibile to find any action with the provided values")


		database.close()


	def delete(self):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - Action class"

		database = Database()
		database.open()

		query = "DELETE FROM actions WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["category"] = self.category
		response["actionName"] = self.actionName
		response["ruleConsequent"] = self.ruleConsequent
		response["description"] = self.description

		return response	

	def __str__(self):
		return "Action " + str(json.dumps(self.getDict(), separators=(',',':')))