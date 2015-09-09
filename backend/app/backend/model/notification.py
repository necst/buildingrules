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
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Notification:
	def __init__(self, id = None, sendTimestamp = None, messageSubject = None, messageText = None, recipientUuid = None, messageRead = None):

			self.id = id
			self.sendTimestamp = sendTimestamp
			self.messageSubject = messageSubject
			self.messageText = messageText
			self.recipientUuid = recipientUuid
			self.messageRead = messageRead

	def setAsRead(self):
		
		if not self.id:
			raise ClassNotInitializedError("You must retrieve the notification from the db to perform a setAsRead or setAsUnRead operation")

		self.messageRead = 1
		self.store()

	def setAsUnRead(self):

		if not self.id:
			raise ClassNotInitializedError("You must retrieve the notification from the db to perform a setAsRead or setAsUnRead operation")

		self.messageRead = 0
		self.store()


	def __replaceSqlQueryToken(self, queryTemplate):

		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.sendTimestamp	!= None	:	queryTemplate = queryTemplate.replace("@@send_timestamp@@", self.sendTimestamp.strftime('%Y-%m-%d %H:%M:%S'))
		if self.messageSubject	!= None	: 	queryTemplate = queryTemplate.replace("@@message_subject@@", self.messageSubject)
		if self.messageText		!= None	: 	queryTemplate = queryTemplate.replace("@@message_text@@", self.messageText)
		if self.recipientUuid	!= None	: 	queryTemplate = queryTemplate.replace("@@recipient_uuid@@", str(self.recipientUuid))
		if self.messageRead		!= None	: 	queryTemplate = queryTemplate.replace("@@message_read@@", str(int(self.messageRead)))

		return queryTemplate

	def store(self):

		if not self.sendTimestamp:
			self.sendTimestamp = datetime.datetime.now() 

		if not self.messageRead:
			self.messageRead = 0

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM notifications WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			query = "UPDATE notifications SET send_timestamp = '@@send_timestamp@@', message_subject = '@@message_subject@@', message_text = '@@message_text@@', recipient_uuid = '@@recipient_uuid@@', message_read = '@@message_read@@' WHERE id = '@@id@@';"
		else:
			query = "INSERT INTO notifications (send_timestamp, message_subject, message_text, recipient_uuid, message_read) VALUES ('@@send_timestamp@@', '@@message_subject@@', '@@message_text@@', '@@recipient_uuid@@', '@@message_read@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):


		if self.id:
			query = "SELECT * FROM notifications WHERE id = '@@id@@';"
		elif self.recipientUuid:
			query = "SELECT * FROM notifications WHERE recipient_uuid = '@@recipient_uuid@@';"
		else:
			raise MissingInputDataError("Impossibile to query any notification with missing parameters")

		database = Database()
		database.open()

		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if len(queryResult)>0:
			self.id = queryResult[0][0]
			self.sendTimestamp = queryResult[0][1]
			self.messageSubject = queryResult[0][2]
			self.messageText = queryResult[0][3]
			self.recipientUuid = queryResult[0][4]
			self.messageRead = queryResult[0][5]
		else:
			database.close()
			raise TriggerNotFoundError("Impossibile to find any notifications with the provided values")

		database.close()

	def delete(self):

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - Trigger class"

		database = Database()
		database.open()

		query = "DELETE FROM notifications WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()


	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["sendTimestamp"] = self.sendTimestamp.strftime('%Y-%m-%d %H:%M:%S')
		response["messageSubject"] = self.messageSubject
		response["messageText"] = self.messageText
		response["recipientUuid"] = self.recipientUuid
		response["messageRead"] = self.messageRead

		return response	

	def __str__(self):
		return "Notification " + str(json.dumps(self.getDict(), separators=(',',':')))