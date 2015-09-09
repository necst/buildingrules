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

class Session:
	def __init__(self, sessionKey = None, userUuid = None, expireTimestamp = None):

		self.sessionKey = sessionKey
		self.userUuid = userUuid
		self.expireTimestamp = expireTimestamp

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.sessionKey 			!= None	: 	queryTemplate = queryTemplate.replace("@@session_key@@", str(self.sessionKey))
		if self.userUuid 			!= None	: 	queryTemplate = queryTemplate.replace("@@user_uuid@@", str(self.userUuid))
		if self.expireTimestamp		!= None	:	queryTemplate = queryTemplate.replace("@@expire_timestamp@@", self.expireTimestamp.strftime('%Y-%m-%d %H:%M:%S'))

		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		query = "INSERT INTO sessions (session_key, user_uuid, expire_timestamp) VALUES ('@@session_key@@', '@@user_uuid@@', '@@expire_timestamp@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if self.userUuid is None and self.sessionKey:
			query = "SELECT * FROM sessions WHERE session_key = '@@session_key@@';"
		elif self.userUuid and not self.sessionKey:
			query = "SELECT * FROM sessions WHERE user_uuid = '@@user_uuid@@';"
		else:
			query = "SELECT * FROM sessions WHERE session_key = '@@session_key@@' AND user_uuid = '@@user_uuid@@';"



		database = Database()
		database.open()

		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if len(queryResult) > 0:
			self.sessionKey = queryResult[0][0]
			self.userUuid = int(queryResult[0][1])
			self.expireTimestamp = queryResult[0][2]
		else:
			database.close()
			raise SessionNotFoundError("Impossibile to find any session with the provided values")

		database.close()


	def delete(self):

		database = Database()
		database.open()

		query = "DELETE FROM sessions WHERE session_key = '@@session_key@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()


	def getDict(self):
		
		response = {}

		response["sessionKey"] = self.sessionKey
		response["userUuid"] = self.userUuid
		response["expireTimestamp"] = self.expireTimestamp

		return response	

	def __str__(self):
		return "Session " + str(json.dumps(self.getDict(), separators=(',',':')))