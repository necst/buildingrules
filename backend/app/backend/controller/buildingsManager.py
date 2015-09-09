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
from app.backend.model.building import Building
from app.backend.model.buildings import Buildings

class BuildingsManager:
	def __init__(self):
		pass

	def getInfo(self, buildingName):
		checkData(locals())
	
		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.getDict()

	def getAllBuildings(self):
		checkData(locals())

		buildings = Buildings()
		buildingList = []

		for building in buildings.getAllBuildings():
			buildingList.append(building.getDic())

		return {"buildings" : buildingList}

	def checkUserBinding(self, buildingName, username):
		checkData(locals())


		from app.backend.model.user import User

		building = Building(buildingName = buildingName)
		building.retrieve()

		user = User(username = username)
		user.retrieve()

		building.checkUserBinding(user)

	def getGroups(self, buildingName, username = None):
		checkData(locals())

		building = Building(buildingName = buildingName)
		building.retrieve()

		groupList = []

		if username:
			from app.backend.model.user import User
			user = User(username = username)
			user.retrieve()

			for buildingGroup in building.getGroups():
				for userGroup in user.getGroups():
					if buildingGroup.buildingName == userGroup.buildingName and buildingGroup.id == userGroup.id:
						groupList.append(userGroup.getDict())
		else:
			for group in building.getGroups():
				groupList.append(group.getDict())

		return {"groups" : groupList}

	def getCrossRoomValidationGroups(self, buildingName, roomName = None, validationCategories = None):
		checkData(locals())

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.getCrossRoomValidationGroups(roomName = roomName, validationCategories = validationCategories)	

	def getRooms(self, buildingName, username = None):
		checkData(locals())

		building = Building(buildingName = buildingName)
		building.retrieve()

		roomList = []

		if username:
			from app.backend.model.user import User
			user = User(username = username)
			user.retrieve()

			for buildingRoom in building.getRooms():
				for userRoom in user.getRooms():
					if buildingRoom.buildingName == userRoom.buildingName and buildingRoom.roomName == userRoom.roomName:
						roomList.append(userRoom.getDict())
		else:

			for room in building.getRooms():
				roomList.append(room.getDict())


		return {"rooms" : roomList}

	def getUnassignedRooms(self, buildingName):
		checkData(locals())

		building = Building(buildingName = buildingName)
		building.retrieve()

		roomList = []

		for room in building.getUnassignedRooms():
			roomList.append(room.getDict())

		return {"rooms" : roomList}


	def addRoom(self, roomName, buildingName, description):
		checkData(locals())

		
		from app.backend.model.room import Room
		room = Room(roomName = roomName,  buildingName = buildingName, description = description)

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.addRoom(room).getDict()
		
	def addGroup(self, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories):
		checkData(locals(), ["crossRoomsValidationCategories"])
		if crossRoomsValidation: checkData(json.loads(crossRoomsValidationCategories))

		return self.__addOrModifyGroup(buildingName = buildingName, description =description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories)


	def deleteRoom(self, buildingName, roomName):
		checkData(locals())

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  not yet tested"
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  table rules_priority not correctly updated"

		from app.backend.model.room import Room
		room = Room(roomName = roomName,  buildingName = buildingName)
		room.retrieve()

		ruleList = room.getRules()
		triggerList = room.getTriggers()
		actionList = room.getActions()

		for rule in ruleList:
			rule.delete()

		for trigger in triggerList:
			room.deleteTrigger(trigger)

		for action in actionList:
			room.deleteAction(action)

		room.delete()

		return {}

	def deleteGroup(self, buildingName, groupId):
		checkData(locals())

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  not yet tested"

		from app.backend.model.group import Group
		group = Group(buildingName = buildingName, id = groupId)

		roomList = group.getRooms()
		ruleList = group.getRules()

		for room in roomList:
			group.deleteRoom(room)

		for rule in ruleList:
			rule.delete()

		group.delete()

		return {}


	def editGroup(self, groupId, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories):
		checkData(locals(), ["crossRoomsValidationCategories"])
		if crossRoomsValidation: checkData(json.loads(crossRoomsValidationCategories))
		
		return self.__addOrModifyGroup(buildingName = buildingName, description =description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories, groupId = groupId)

	def __addOrModifyGroup(self, buildingName, description, crossRoomsValidation, crossRoomsValidationCategories, groupId = None):


		if type(crossRoomsValidation) == int:
			crossRoomsValidation = bool(crossRoomsValidation)
		elif type(crossRoomsValidation) == str or type(crossRoomsValidation) == unicode:

			if str(crossRoomsValidation.upper()) == "TRUE" or str(crossRoomsValidation.upper()) == "1":
				crossRoomsValidation = True
			else:
				crossRoomsValidation = False

		elif type(crossRoomsValidation) != bool:
			raise IncorrectInputDataTypeError("crossRoomsValidation must be a booelan value (True,False) or integer value (1,0)")


		if not crossRoomsValidation:
			crossRoomsValidationCategories = []
		else:
			crossRoomsValidationCategories = json.loads(crossRoomsValidationCategories)


		if crossRoomsValidation and len(crossRoomsValidationCategories) == 0:
			raise MissingInputDataError("Selecting crossRoomsValidation you need to insert at least one rule category in crossRoomsValidationCategories")

		from app.backend.model.group import Group
		group = Group(id = groupId, buildingName = buildingName, description = description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories)

		building = Building(buildingName = buildingName)
		building.retrieve()

		return building.addGroup(group).getDict()


	def __str__(self):
		return "BuildingsManager: "