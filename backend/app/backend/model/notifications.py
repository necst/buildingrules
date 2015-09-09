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
from app.backend.model.notification import Notification

class Notifications:
	def __init__(self):
		pass

	def retrieveNotifications(self, user = None, userUuid = None, excludeRead = True):

		if not user and not userUuid:
			raise MissingInputDataError("Cannot retrieve notifications without user or useruuid")

		if user:
			userUuid = user.uuid

		query = "SELECT * FROM notifications WHERE recipient_uuid = '@@recipient_uuid@@' and message_read = '0';"
		if not excludeRead:
			query = "SELECT * FROM notifications WHERE recipient_uuid = '@@recipient_uuid@@';"

		query = query.replace("@@recipient_uuid@@", userUuid)

		notificationList = []

		database = Database()
		database.open()
		queryResult = database.executeReadQuery(query)

		for record in queryResult:
			notificationId = record[0]
			sendTimestamp = record[1]
			messageSubject = record[2]
			messageText = record[3]
			recipientUuid = record[4]
			messageRead = record[5]

			notification = Notification(id = notificationId, sendTimestamp = sendTimestamp, messageSubject = messageSubject, messageText = messageText, recipientUuid = recipientUuid, messageRead = messageRead)
			notificationList.append(notification)

		database.close()
		return notificationList

	def __str__(self):
		return "Notifications: "