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
from app.backend.model.user import User
from app.backend.model.users import Users


class UsersManager:
	def __init__(self):
		pass

	def getUser(self, username, password = None):
		checkData(locals())
		
		user = User(username = username, password = password)		
		user.retrieve()
		return user

	def getInfo(self, username = None, uuid = None):
		checkData(locals())
		
		if username:
			user = User(username = username)		
			user.retrieve()

			return user.getDict()
		elif uuid:
			user = User(uuid = uuid)		
			user.retrieve()

			return user.getDict()
		else:
			raise MissingInputDataError("You need to specify at least the username or the uuid to gather user information")

	def registerTemporary(self, newUserUsername, newUserPassword, newUserEmail, newUserPersonName, newUserLevel = 10):
		checkData(locals())

		try:
			user = User(username = newUserUsername)
			user.retrieve()
			raise UsernameNotAvailableError("The username " + newUserUsername + " has been alredy assigned")

		except UserNotFoundError as e:
		
			if not(newUserUsername and newUserPassword and newUserEmail and newUserPersonName and newUserLevel):
				raise MissingInputDataError("Some input data are missing to register a new user")

			users = Users()
			freeUserSlot = users.getFirstFreeUserSlot()

			freeUserSlot.username = newUserUsername
			freeUserSlot.password = newUserPassword
			freeUserSlot.email = newUserEmail
			freeUserSlot.personName = newUserPersonName
			freeUserSlot.store()

			return freeUserSlot.getDict()

			#user = User(username = newUserUsername, password = newUserPassword, email = newUserEmail, personName = newUserPersonName, level = newUserLevel)
			#user.store()

			#return user.getDict()


	def register(self, creatorUuid, newUserUsername, newUserPassword, newUserEmail, newUserPersonName, newUserLevel):
		checkData(locals())

		creatorUser = User(uuid = creatorUuid)		
		creatorUser.retrieve()

		if creatorUser.level != 0:
			raise UserCredentialError("Only root user can create new users")

		try:
			user = User(username = newUserUsername)
			user.retrieve()
			raise UsernameNotAvailableError("The username " + newUserUsername + " has been alredy assigned")

		except UserNotFoundError as e:
		
			if not(newUserUsername and newUserPassword and newUserEmail and newUserPersonName and newUserLevel):
				raise MissingInputDataError("Some input data are missing to register a new user")

			user = User(username = newUserUsername, password = newUserPassword, email = newUserEmail, personName = newUserPersonName, level = newUserLevel)
			user.store()

			return user.getDict()


	def getBuildingList(self, username):
		checkData(locals())

		user = User(username = username)		
		user.retrieve()

		response = []
		buildingList = user.getBuildings()
		for building in buildingList:
			response.append(building.getDict())
			

		return {"buildings" : response}

	def getRoomList(self, username):
		checkData(locals())

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : not yet tested"

		user = User(username = username)		
		user.retrieve()

		return user.getRooms()

	def addRoom(self, username):
		checkData(locals())
		
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : not yet implemented"

	def __str__(self):
		return "UserManager: "