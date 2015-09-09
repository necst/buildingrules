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
import MySQLdb
import json
import datetime

class Test:
	def __init__(self):
		pass


	def test6(self):

		print "hi i'm here!!"

		from app.backend.model.buildings import Buildings		
		from app.backend.controller.rulesetChecker import RulesetChecker	
		import random	
		import time,datetime
		from app.backend.commons.console import flash

		buildings = Buildings()
		
		for building in buildings.getAllBuildings():
			buildingRules = building.getRules()


			for ruleNumber in range(0,81):		
				print "Testing with ruleNumber " + str(ruleNumber)
				for testNumber in range(0, 250):
					print "Testing with ruleNumber " + str(ruleNumber) + " #iteration: " + str(testNumber)
					tmpRuleSet = []
					tmpRuleIndex = []

					#Creating the temporary ruleset
					for i in range(0, ruleNumber):
						selectedRule = random.randint(0,len(buildingRules)-1)
						if selectedRule not in tmpRuleIndex:
							tmpRuleIndex.append(selectedRule)
							tmpRuleSet.append(buildingRules[selectedRule])

					rulesetChecker = RulesetChecker(tmpRuleSet)
		
					startTimeMilliseconds = long((time.time() + 0.5) * 1000)
					ruleCheckErrorList = rulesetChecker.check()
					endTimeMilliseconds = long((time.time() + 0.5) * 1000)
					
					opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds

					if len(ruleCheckErrorList) == 0:
						flash("EXPERIMENT-TestRoomRuleVerification [SUCCESS]:" + "#rules=" + str(ruleNumber) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))
					else:
						flash("EXPERIMENT-TestRoomRuleVerification [FAILED]:" + "#rules=" + str(ruleNumber) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))

			print "DONE."
						

	def test5(self):
		from app.backend.controller.buildingSimulator import BuildingSimulator		

		buildingSimulator = BuildingSimulator(buildingName = "CSE", startDate = "2014-02-15", numberOfDays = 7, roomFilter = None)
		buildingSimulator.start()

	def test4(self):
		from app.backend.controller.roomSimulator import RoomSimulator		

		roomSimulator = RoomSimulator(occupancyTimeRangeFrom = "4:00AM", occupancyTimeRangeTo = "6:00PM", buildingName = "CSE", roomName = "3208", roomTemperature = "78F", externalTemperature = "75F", weather = "Sunny")
		roomSimulator.start()

	def test3(self):

		from app.backend.controller.triggerManager import TriggerManager

		triggerManager = TriggerManager()
		translatedTriggers = triggerManager.translateTrigger("someone is in the room, it is cloudy, it is rainy, time is between 10:00 and 11:00")

		print translatedTriggers["translation"]

		for trigger in translatedTriggers["triggers"]:
			print trigger["translation"]
			print trigger["trigger"]
			print trigger["translatedParams"]

		ruleList = []
		from app.backend.model.rule import Rule
		ruleList.append(Rule())


	def test2(self):
		
		from app.backend.model.room import Room
		room = Room(buildingName="EEE", roomName="200")
		ruleList = room.getRules()

		from app.backend.controller.rulesetChecker import RulesetChecker
		rulesetChecker = RulesetChecker(ruleList)
		rulesetChecker.check()


	def test1(self):

		from app.backend.controller.triggerManager import TriggerManager
		from app.backend.controller.actionManager import ActionManager

		triggerManager = TriggerManager()
		print triggerManager.getTrigger("it is between 10.00 AM and 8.00 PM")
		print triggerManager.translateTrigger("it is between 10.00 AM and 8.00 PM")

		actionManager = ActionManager()
		print actionManager.getAction("turn on the heating")




	def test0(self):

		from app.backend.commons.database import Database
		from app.backend.model.building import Building
		from app.backend.model.group import Group
		from app.backend.model.room import Room
		from app.backend.model.user import User
		from app.backend.model.rule import Rule

		print "Starting test..."
		print "Cleaning database..."

		database = Database()
		database.open()
		database.executeWriteQuery("TRUNCATE TABLE buildings")
		database.executeWriteQuery("TRUNCATE TABLE groups")
		database.executeWriteQuery("TRUNCATE TABLE rooms")
		database.executeWriteQuery("TRUNCATE TABLE users")
		database.executeWriteQuery("TRUNCATE TABLE users_rooms")
		database.executeWriteQuery("TRUNCATE TABLE rooms_groups")
		database.executeWriteQuery("TRUNCATE TABLE rules")
		database.close()

		print "Testing model..."

		building = Building(buildingName = "CSE", label = "Computer Science", description = "This is a nice place")
		building.store()

		building = Building(buildingName = "CSE", label = "Computer Science", description = "This is a great place")
		building.store()

 		building = Building(buildingName = "CSE")
 		building.retrieve()
 		print building

 		group = Group(buildingName = "CSE", description = "Questo gruppo eheh")
 		group.store()
 		print group

 		group = Group(id=1, buildingName = "CSE")
 		group.retrieve()
 		print group

 		group = Group(id=1, buildingName = "CSE", description = "we ciao ciao")
 		group.store()

 		group = Group(id=1, buildingName = "CSE")
 		group.retrieve()
 		print group

		room = Room(roomName = "200",  buildingName = "CSE", description = "Bella 3333")
		room.store()

		room = Room(roomName = "200",  buildingName = "CSE")
		room.retrieve()
		print room

		print "room.getBuilding() test"
		print room.getBuilding()

		user = User(username = "alenacci", email = "alenacci@gmail.com", password = "1234", personName = "Alessandro Nacci", level = 10)
		user.store()

		room.addUser(user)

		print "user.getRooms() test"
		for room in user.getRooms():
			print room

		print "group.addRoom(room) test"
		group.addRoom(room)
		
		print group

		print "User test 1"
		user = User(username = "alenacci")
		user.retrieve()
		print user

		print "User test 2"
		user = User(username = "alenacci", password="1234")
		user.retrieve()
		print user

		print "User test 3"
		user = User(uuid = 1)
		user.retrieve()
		print user

		

		rule = Rule(priority = 1, category = "ELECTRICT222", buildingName = "CSE", groupId = 1, roomName = "200", 
				authorUuid = 1, antecedent = "the ligjt is on", consequent = "turn off the light", enabled = 1, deleted = 0)

		rule.store()

		rule = Rule(id = 1)
		rule.retrieve()

		print rule
		print rule.getBuilding()
		print rule.getGroup()
		print rule.getAuthor()

		print "test group.getRules()"
		ruleList = group.getRules()
		for r in ruleList:
			print r

		print "test room.getRules()"
		ruleList = room.getRules()
		for r in ruleList:
			print r

		print "test room.getRules(author)"
		ruleList = room.getRules(author = user, includeGroupsRules = None)
		for r in ruleList:
			print r

		print "test room.getRules(includeGroupsRules)"
		ruleList = room.getRules(includeGroupsRules = True)
		for r in ruleList:
			print r

		print "test user.getCreatedRules()"
		ruleList = user.getCreatedRules()
		for r in ruleList:
			print r

		group.deleteRoom(room)
		room.deleteUser(user)
		rule.delete()
		user.delete()
		group.delete()
		building.delete()
		room.delete()

		user = User(username = "alenacci")
		user.retrieve()

