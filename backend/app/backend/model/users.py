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
from app.backend.model.user import User

class Users:
	def __init__(self):
		pass

	def getAllUsers(self):

		userList = []

		database = Database()
		query = "SELECT * FROM users;"
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		for record in queryResult:
			uuid = record[0]
			username = record[1]
			email = record[2]
			password = record[3]
			personName = record[4]
			level = record[5]

			user = User(uuid = uuid, username = username, email = email, password = password, personName = personName, level = level)

			userList.append(user)

		
		return userList

	def getFirstFreeUserSlot(self):

		print "TODO REMOVE THIS METHOD - NEEDED ONLY FOR THE EXPERIMENTS"

		userList = []

		database = Database()
		query = "SELECT * FROM users WHERE password='verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword' LIMIT 1;"
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		if len(queryResult) == 0:
			raise UserNotFoundError("No more slots available for new users. Thanks for your help! See ya!")

		for record in queryResult:
			uuid = record[0]
			username = record[1]
			email = record[2]
			password = record[3]
			personName = record[4]
			level = record[5]
			registrationTimestamp = datetime.datetime.now()

			user = User(uuid = uuid, username = username, email = email, password = password, personName = personName, level = level, registrationTimestamp = registrationTimestamp)
			user.store()
			return user


	def __str__(self):
		return "Users: "