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
import os
import time
import datetime
import urllib2
import shutil
from app.backend.commons.console import flash
from app.backend.commons.errors import *

from app.backend.model.users import Users
from app.backend.controller.notificationsManager import NotificationsManager



__SERVICE_FILE_PATH = "tools/weather/"

def start():
	flash("BuildingRules MailService is active...")
	while(1):
		try:
			main()
		except Exception as e:
			import logging
			logging.exception("")
			flash(e.message)

		time.sleep(43200)
		

def main():

	flash("Getting user list...")

	users = Users()
	userList = users.getAllUsers()

	notificationsManager = NotificationsManager()

	for user in userList:
		
		flash("Looking for " + str(user.uuid) + ":" + user.username + " notifications...")
		
		notificationList = notificationsManager.getNotifications(userUuid = str(user.uuid), username = user.username, automaticallySetAsRead = False)


		if len(notificationList["notifications"]):

			recipientUuid = notificationList["notifications"][0]["recipientUuid"]

			messageText = ""
			
			for notification in notificationList["notifications"]:
				messageText += notification["messageSubject"] + " (" + notification["sendTimestamp"] + ")" + "\n"
				messageText += "----------------------------------------------------" + "\n"
				messageText += notification["messageText"] + "\n"
				messageText += "\n\n\n"

		
			messageSubject = "[BUILDING RULES] - Notifications report"
			flash("Sending report to " + str(user.uuid) + ":" + user.username + ":" + user.email)
			notificationsManager.sendNotificationByEmail(recipientUuid = recipientUuid, messageSubject = messageSubject, messageText = messageText)