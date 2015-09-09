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
import datetime
import time
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Feedback:
	def __init__(self, id = None, authorUuid = None, alternativeContact = None, score = None, message = None, feedbackTimestamp = None):

			self.id = id
			self.authorUuid = authorUuid
			self.alternativeContact = alternativeContact
			self.score = score
			self.message = message
			self.feedbackTimestamp = feedbackTimestamp

	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id 					!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.authorUuid			!= None	: 	queryTemplate = queryTemplate.replace("@@author_uuid@@", str(self.authorUuid))		
		if self.alternativeContact	!= None	: 	queryTemplate = queryTemplate.replace("@@alternative_contact@@", str(self.alternativeContact))
		if self.score				!= None	: 	queryTemplate = queryTemplate.replace("@@score@@", str(self.score))
		if self.message 			!= None	: 	queryTemplate = queryTemplate.replace("@@message@@", str(self.message))
		if self.feedbackTimestamp	!= None	:	queryTemplate = queryTemplate.replace("@@feedback_timestamp@@", self.feedbackTimestamp.strftime('%Y-%m-%d %H:%M:%S'))

		return queryTemplate

	def store(self):

		if not self.feedbackTimestamp:
			self.feedbackTimestamp = datetime.datetime.now() 


		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM feedbacks WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE feedbacks SET author_uuid = '@@author_uuid@@', alternative_contact = '@@alternative_contact@@', score = '@@score@@', message = '@@message@@', feedback_timestamp = '@@feedback_timestamp@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO feedbacks (author_uuid, alternative_contact, score, message, feedback_timestamp) VALUES ('@@author_uuid@@', '@@alternative_contact@@', '@@score@@', '@@message@@', '@@feedback_timestamp@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		self.id = int(database.getLastInsertedId()) if not self.id else self.id
		database.close()


	def retrieve(self):

		if self.id:
			query = "SELECT * FROM feedbacks WHERE id = '@@id@@';"
		else:
			raise MissingInputDataError("Impossibile to query any feedback with missing parameters")

		database = Database()
		database.open()
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if len(queryResult) > 0:
			self.id = queryResult[0][0]
			self.authorUuid = queryResult[0][1]
			self.alternativeContact = queryResult[0][2]
			self.score = queryResult[0][3]
			self.message = queryResult[0][4]
			self.feedbackTimestamp = queryResult[0][5]
		else:
			database.close()
			raise MturkNotFoundError("Impossibile to find any feedback with the provided values")

		database.close()

	def delete(self):

		database = Database()
		database.open()

		query = "DELETE FROM feedbacks WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["authorUuid"] = self.authorUuid
		response["alternativeContact"] = self.alternativeContact
		response["score"] = self.score
		response["message"] = self.message
		response["feedbackTimestamp"] = self.feedbackTimestamp.strftime('%Y-%m-%d %H:%M:%S') if self.feedbackTimestamp else None

		return response	


	def __str__(self):
		return "Feedback " + str(json.dumps(self.getDict(), separators=(',',':')))