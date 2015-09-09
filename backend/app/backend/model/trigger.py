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

class Trigger:
	def __init__(self, id = None, category = None, triggerName = None, ruleAntecedent = None, description = None):

			self.id = id
			self.category = category
			self.triggerName = triggerName
			self.ruleAntecedent = ruleAntecedent
			self.description = description

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.category 		!= None	: 	queryTemplate = queryTemplate.replace("@@trigger_name@@", self.category)
		if self.triggerName 	!= None	: 	queryTemplate = queryTemplate.replace("@@trigger_name@@", self.triggerName)
		if self.ruleAntecedent	!= None	: 	queryTemplate = queryTemplate.replace("@@rule_antecedent@@", self.ruleAntecedent)
		if self.description		!= None	: 	queryTemplate = queryTemplate.replace("@@description@@", self.description)

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM triggers WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE triggers SET category = '@@category@@', trigger_name = '@@trigger_name@@', rule_consequent = '@@rule_consequent@@', description = '@@description@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO triggers (category, trigger_name, rule_consequent, description) VALUES ('@@category@@', '@@trigger_name@@', '@@rule_consequent@@', '@@description@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):


		if self.id:
			query = "SELECT * FROM triggers WHERE id = '@@id@@';"
		elif self.triggerName:
			query = "SELECT * FROM triggers WHERE trigger_name = '@@trigger_name@@';"
		else:
			raise MissingInputDataError("Impossibile to query any trigger with missing parameters")

		database = Database()
		database.open()

		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)



		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.category = queryResult[0][1]
			self.triggerName = queryResult[0][2]
			self.ruleAntecedent = queryResult[0][3]
			self.description = queryResult[0][4]
		else:
			database.close()
			raise TriggerNotFoundError("Impossibile to find any trigger with the provided values")

		database.close()

	def delete(self):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - Trigger class"

		database = Database()
		database.open()

		query = "DELETE FROM triggers WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["category"] = self.category
		response["triggerName"] = self.triggerName
		response["ruleAntecedent"] = self.ruleAntecedent
		response["description"] = self.description

		return response	


	def __str__(self):
		return "Trigger " + str(json.dumps(self.getDict(), separators=(',',':')))