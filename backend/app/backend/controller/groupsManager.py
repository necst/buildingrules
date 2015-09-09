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
from app.backend.model.group import Group

class GroupsManager:
	def __init__(self):
		pass

	def getInfo(self, groupId, buildingName):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()
		return group.getDict()


	def getRules(self, groupId, buildingName):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		ruleList = group.getRules()

		response = []
		for rule in ruleList:
			response.append(rule.getDict())
			
		return {"rules" : response}

	def isCrossRoomsValidationGroup(self, groupId, buildingName, crossRoomsValidationCategory = None):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		if group.crossRoomsValidation:		

			if crossRoomsValidationCategory:
				if crossRoomsValidationCategory in group.crossRoomsValidationCategories:
					return True
				else:
					return False
			else:
				return True

		else:
			return False

	def getRooms(self, groupId, buildingName):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		roomList = []
		for room in group.getRooms():
			roomList.append(room.getDict())

		return {"rooms" : roomList}		

	def addRoom(self, groupId, roomName, buildingName):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		from app.backend.model.room import Room
		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()


		if group.crossRoomsValidation:
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  This part of the method as not been tested"
			# In this case we have to check that the room doesn't belong to another CrossRoomValidatioGroup
			from app.backend.model.building import Building
			building = Building(buildingName = buildingName)
			building.retrieve()
			crvgList = building.getCrossRoomValidationGroups(roomName = roomName, validationCategories = group.crossRoomsValidationCategories)

			if len(crvgList) > 0:
				raise WrongBuildingGroupRipartitionError("A room can belong to only one cross validation group per category. Room " + str(roomName) + " in already in group " + str(crvgList[0]))

		group.addRoom(room)

		return room.getDict()

	def addRule(self, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):
		checkData(locals())

		return self.__addOrModifyRule(priority = priority, buildingName = buildingName, groupId = groupId,  authorUuid = authorUuid, ruleBody = ruleBody)

	def editRule(self, ruleId = None, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None):

		from app.backend.model.rule import Rule
		oldRule = Rule(id = ruleId)
		oldRule.retrieve()

		from app.backend.model.user import User
		author = User(uuid = authorUuid)
		author.retrieve()

		result = self.__addOrModifyRule(ruleId = ruleId, priority = priority, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, ruleBody = ruleBody)

		from app.backend.controller.notificationsManager import NotificationsManager
		notifications = NotificationsManager()
		messageSubject = "Rule modified in building " + str(buildingName) + " group " + str(groupId)
		messageText = "The user " + str(author.username) + " edited (or tried to edit) the rule <<" + str(oldRule.getFullRepresentation()) + ">>. The new rule is <<" + str(ruleBody) + ">>"
		notifications.sendNotification(buildingName = buildingName, groupId = groupId, messageSubject = messageSubject, messageText = messageText) 

		return result
		

	def deleteRule(self, ruleId, buildingName, groupId):
		checkData(locals())

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		group.deleteRule(rule)

		return {}

	def getRuleInfo(self, buildingName = None, groupId = None, ruleId = None):
		checkData(locals())

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, groupId = groupId)
		rule.retrieve()

		return rule.getDict()

	def getTriggers(self, buildingName = None, groupId = None):
		checkData(locals())

		from app.backend.model.triggers import Triggers
		triggers = Triggers()

		triggerList = []
		for trigger in triggers.getAllTriggers():
			triggerList.append(trigger.getDict())

		return {"triggers" : triggerList}


	def getActions(self, buildingName = None, groupId = None):
		checkData(locals())

		from app.backend.model.actions import Actions
		actions = Actions()

		actionList = []
		for action in actions.getAllActions():
			actionList.append(action.getDict())

		return {"actions" : actionList}


	def __addOrModifyRule(self, priority = None, buildingName = None, groupId = None, authorUuid = None, ruleBody = None, ruleId = None):
		checkData(locals())

		import time,datetime
		startTimeMilliseconds = long((time.time() + 0.5) * 1000)
		

		try:
			antecedent = ruleBody.split("then")[0].replace("if ", "").strip()
			consequent = ruleBody.split("then")[1].strip()
		except Exception as e:
			raise NotWellFormedRuleError("There is a syntax error in the rule you are trying to save")

		from app.backend.controller.actionManager import ActionManager
		actionManager = ActionManager()
		category = actionManager.getAction(consequent).category

		from app.backend.model.user import User
		author = User(uuid = authorUuid)
		author.retrieve()

		if int(str(priority)) < 0 or int(str(priority)) > author.getMaxGroupPriority():
			raise RulePriorityError("You can specify rules for groups with a priority value between 0 and " + str(author.getMaxRoomPriority()) + ". You inserted " + str(priority))

		from app.backend.model.rule import Rule
		from app.backend.model.group import Group

		if not ruleId:
			rule = Rule(priority = priority, category = category, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, antecedent = antecedent, consequent = consequent, enabled = True)
		else:
			rule = Rule(id = ruleId)
			rule.retrieve()
			author = rule.getAuthor()

			
			rule.antecedent = antecedent
			rule.consequent = consequent
			rule.authorUuid = authorUuid

			editor = rule.getAuthor()

			if editor.level < rule.getPriority():
				raise UserCredentialError("You cannot modify this rule since it has a too high priority for your user level")

		group = Group(buildingName = buildingName, id = groupId)
		group.retrieve()

		if not ruleId and not rule.checkIfUnique():
			raise DuplicatedRuleError("The submitted rule is already been saved for the considered group.")

		# excludedRuleId is needed to ignore the rule that the user want to edit
		excludedRuleId = ruleId if ruleId else None		


		ruleCheckErrorList = []
		groupRoomList = group.getRooms()
		for room in groupRoomList:

			groupRules = group.getRules(excludedRuleId = excludedRuleId)

			# Checking that a priority is unique over the same category	
			for r in groupRules:
				if str(r.category) == str(category) and int(r.getPriority()) == int(priority):
					raise AlredyAssignedPriorityError("In group " + str(groupId) + " the priority " + str(priority) + " has alredy been assigned to another rule with the same category!")


			temporaryRuleSet = []
			temporaryRuleSet.extend(room.getRules(author = False, includeGroupsRules = True, excludedRuleId = False, excludeCrossRoomValidationRules = True))
			temporaryRuleSet.extend(groupRules)

			temporaryRuleSet.append(rule)


			from app.backend.controller.rulesetChecker import RulesetChecker
			rulesetChecker = RulesetChecker(temporaryRuleSet)

			ruleCheckErrorList.extend(rulesetChecker.check())

		if len(ruleCheckErrorList) == 0:
			
			if ruleId: 	#if i'm in edit mode
				rule.id = ruleId
				rule.setPriority(priority)

			# Disabling rules in all the groups rooms since they have to be validated again

			for room in groupRoomList:
			
				from app.backend.controller.notificationsManager import NotificationsManager
				notifications = NotificationsManager()
				messageSubject = "Group " +  str(groupId) + " changed your room " + str(room.roomName) + " policy."
				messageText =  "Some rules in group " + str(groupId) + " have been changed."
				notifications.sendNotification(buildingName = buildingName, roomName = room.roomName, messageSubject = messageSubject, messageText = messageText) 
				
				#for r in room.getRules(includeGroupsRules = False, excludeCrossRoomValidationRules = True):
				#	r.disable()

			from app.backend.commons.console import flash
			endTimeMilliseconds = long((time.time() + 0.5) * 1000)
			opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds
			flash("GroupsRuleVerification [SUCCESS]: groupId = " + str(groupId) +" #rules=" + str(len(temporaryRuleSet)) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))

			return group.addRule(rule).getDict()
		else:

			from app.backend.commons.console import flash
			
			logMessage = "authorUuid =  " + str(authorUuid) + ", "
			logMessage += "buildingName =  " + str(buildingName) + ", "
			logMessage += "gropuId =  " + str(groupId) + ", "
			logMessage += "ruleSetDescr =  " + str(temporaryRuleSet) + ", "
			logMessage += "newRule =  " + str(rule)

			flash("RuleValidationError: " + logMessage)

			endTimeMilliseconds = long((time.time() + 0.5) * 1000)
			opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds
			flash("GroupsRuleVerification [FAILED]: groupId = " + str(groupId) +" #rules=" + str(len(temporaryRuleSet)) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))

			raise RuleValidationError(ruleCheckErrorList + " Error in room " + room.roomName)

	def __str__(self):
		return "GroupsManager: "