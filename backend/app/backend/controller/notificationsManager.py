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
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.notification import Notification
from app.backend.model.notifications import Notifications

import imaplib
import smtplib  
import email


class NotificationsManager:
	def __init__(self):
		pass

	def sendNotification(self, userUuid = None, buildingName = None, groupId = None, roomName = None, messageSubject = None, messageText = None):
		checkData(locals())

		
		if not messageSubject:
			raise NewNotificationMissingInputError("messageSubject is mandatory to send a new notification")

		if not messageText:
			raise NewNotificationMissingInputError("messageText is mandatory to send a new notification")

		if not userUuid and not buildingName:
			raise NewNotificationMissingInputError("You have to specify at least one recipient to send a new notification")

		if buildingName and not roomName and not groupId:
			raise NewNotificationMissingInputError("You cannot send a notification to an entire building. You have to specify at least a room or a group.")			

		if not buildingName and not roomName and not groupId:
			raise NewNotificationMissingInputError("You have to specify at least one recipient to send a new notification.")			


		recipientUuidList = []

		if userUuid:
			recipientUuidList.append(userUuid)

		if buildingName and roomName:
			from app.backend.model.room import Room

			room = Room(buildingName = buildingName, roomName = roomName)
			room.retrieve()

			for user in room.getUsers():
				recipientUuidList.append(user.uuid)

			# managing rooms insid a cross validation group
			for group in room.getGroups():
				if group.crossRoomsValidation:
					for gRoom in group.getRooms():
						for user in gRoom.getUsers():
							recipientUuidList.append(user.uuid)


		if buildingName and groupId:

			from app.backend.model.group import Group
			from app.backend.model.room import Room

			group = Group(buildingName = buildingName, id = groupId)
			group.retrieve()

			for room in group.getRooms():
				for user in room.getUsers():
					recipientUuidList.append(user.uuid)

		# Removing duplicate Id
		recipientUuidList = list(set(recipientUuidList))

		for recipientUuid in recipientUuidList:
			notification = Notification(recipientUuid = recipientUuid, messageSubject = messageSubject, messageText = messageText)
			notification.store()

		return {}

	def sendNotificationByEmail(self, recipientUuid, messageSubject, messageText):
		checkData(locals())

		from app.backend.model.user import User
		recipientUser = User(uuid = recipientUuid)
		recipientUser.retrieve()
		
		recipient = recipientUser.email
		subject = "[BuldingRules Notification] " + messageSubject
		message = messageText

		self.__send_message(recipient = recipient, subject = subject, message = message)

	def __send_message(self, recipient, subject, message):

		__MAIN_ADDRESS = 'energybox.buildingrules@gmail.com'
		__MAIN_PASSWORD  = 'buildingdepot'

		fromaddr = __MAIN_ADDRESS 
		toaddrs  = recipient

		complete_msg = 'Subject: %s\n\n%s' % (subject, message)
		  
		# The actual mail send  
		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login(__MAIN_ADDRESS,__MAIN_PASSWORD )  
		server.sendmail(fromaddr, toaddrs, complete_msg)  
		server.quit()  


	def setNotificationAsRead(self, notificationId):
		checkData(locals())


		notification = Notification(id = notificationId)	
		notification.setAsRead()
		return {}

	def setNotificationAsUnread(self, notificationId):
		checkData(locals())

		
		notification = Notification(id = notificationId)
		notification.setAsUnread()
		return {}

	def getNotifications(self, userUuid, username, automaticallySetAsRead = True):
		checkData(locals())
		

		from app.backend.model.user import User
		user = User(username = username)
		user.retrieve()

		if str(userUuid) != str(user.uuid):
			raise UserCredentialError("You cannot other users' notifications!")

		
		notifications = Notifications()
		notificationList = []

		for notification in notifications.retrieveNotifications(userUuid = userUuid):
			if automaticallySetAsRead: notification.setAsRead()
			notificationList.append(notification.getDict())
		
		return {"notifications" : notificationList}

	
	def __str__(self):
		return "NotificationManager: "