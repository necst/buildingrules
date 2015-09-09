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

class Setting:
	def __init__(self, key = None, value = None):

		self.key = key
		self.value = value

	def __replaceSqlQueryToken(self, queryTemplate):

		if self.key 			!= None	: 	queryTemplate = queryTemplate.replace("@@s_key@@", str(self.key))
		if self.value 			!= None	: 	queryTemplate = queryTemplate.replace("@@s_value@@", str(self.value))

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(s_key) FROM settings WHERE s_key = '@@s_key@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)



		if int(queryResult[0][0]) > 0:
			query = "UPDATE settings SET s_value = '@@s_value@@' WHERE s_key = '@@s_key@@';"

		else:
			query = "INSERT INTO settings (s_key, s_value) VALUES ('@@s_key@@', '@@s_value@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if self.key:
			query = "SELECT * FROM settings WHERE s_key = '@@s_key@@';"
		else:
			raise MissingInputDataError("Impossibile to query any setting with missing parameters")
			

		database = Database()
		database.open()

		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:

			self.key = queryResult[0][0]
			self.value = queryResult[0][1]

		else:
			database.close()
			raise SettingNotFoundError("Impossibile to find any setting with the key '" + self.key + "'")


		database.close()


	def delete(self):

		database = Database()
		database.open()

		query = "DELETE FROM settings WHERE s_key = '@@s_key@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["key"] = self.key
		response["value"] = self.value
	
		return response	

	def __str__(self):
		return "Setting " + str(json.dumps(self.getDict(), separators=(',',':')))

