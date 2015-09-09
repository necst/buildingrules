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

class Mturk:
	def __init__(self, id = None, day = None, userUuid = None, token = None):

			self.id = id
			self.day = day
			self.userUuid = userUuid
			self.token = token

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 			!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.day		 	!= None	: 	queryTemplate = queryTemplate.replace("@@day@@", str(self.day))
		if self.userUuid 	!= None	: 	queryTemplate = queryTemplate.replace("@@user_uuid@@", str(self.userUuid))
		if self.token		!= None	: 	queryTemplate = queryTemplate.replace("@@token@@", self.token)

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM mturk WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE mturk SET day = '@@day@@', user_uuid = '@@user_uuid@@', token = '@@token@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO mturk (day, user_uuid, token) VALUES ('@@day@@', '@@user_uuid@@', '@@token@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if self.id:
			query = "SELECT * FROM mturk WHERE id = '@@id@@';"
		if self.day != None and self.userUuid != None:
			query = "SELECT * FROM mturk WHERE day = '@@day@@' AND user_uuid = '@@user_uuid@@' ;"
		else:
			raise MissingInputDataError("Impossibile to query any Mturk with missing parameters")

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)



		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.day = queryResult[0][1]
			self.userUuid = queryResult[0][2]
			self.token = queryResult[0][3]
		else:
			database.close()
			raise MturkNotFoundError("Impossibile to find any Mturk with the provided values")

		database.close()

	def delete(self):

		database = Database()
		database.open()

		query = "DELETE FROM mturk WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["day"] = self.day
		response["userUuid"] = self.userUuid
		response["token"] = self.token

		return response	


	def __str__(self):
		return "Mturk " + str(json.dumps(self.getDict(), separators=(',',':')))