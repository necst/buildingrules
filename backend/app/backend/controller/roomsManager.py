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
from app.backend.model.room import Room


class RoomsManager:
	def __init__(self):
		pass

	def getInfo(self, roomName, buildingName):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()
		return room.getDict()

	def getConflictingRules(self, roomName, buildingName, ruleBody):
		checkData(locals())

		ruleBody = ruleBody.strip()

		from app.backend.controller.triggerManager import TriggerManager
		from app.backend.controller.actionManager import ActionManager
		triggerManager = TriggerManager()
		actionManager = ActionManager()

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		ruleList = room.getRules( includeGroupsRules = True,  includeDisabled = False)



		ruleAntecedent = ruleBody.split("then")[0].replace("if", "").strip()
		ruleConsequent = ruleBody.split("then")[1].strip()
		
		newRuleTranslatedTriggers = triggerManager.translateTrigger(ruleAntecedent)
		newRuleAction, originalModel, parameterValues = actionManager.getActionAndTemplateAndParameterValues(ruleConsequent)


		conflictingRuleList = []
		for rule in ruleList:

			currentRuleAction, originalModel, parameterValues = actionManager.getActionAndTemplateAndParameterValues(rule.consequent)
			savedRuleTranslatedTriggers = triggerManager.translateTrigger(rule.antecedent)			

			conflictingAntecedentFound = False
			
			for newRuleTrigger in newRuleTranslatedTriggers["triggers"]:

				for savedRuleTrigger in savedRuleTranslatedTriggers["triggers"]:
					
					if "between" not in newRuleTrigger["antecedent"]:

						if newRuleTrigger["antecedent"] == savedRuleTrigger["antecedent"] and (newRuleAction.category == currentRuleAction.category): 
							conflictingAntecedentFound = True

					else:

						# In the case of range based antecedent I cannot just check if it is equal but I have to see the trigger name
						if newRuleTrigger["trigger"].triggerName == savedRuleTrigger["trigger"].triggerName and (newRuleAction.category == currentRuleAction.category):
							conflictingAntecedentFound = True

					if conflictingAntecedentFound: break
				if conflictingAntecedentFound: break

			if conflictingAntecedentFound:
				conflictingRuleList.append({"ruleId" : rule.id, "ruleBody" : rule.getFullRepresentation()})



		return {"conflictingRules" : conflictingRuleList}


	def getRules(self, roomName, buildingName, username = None, includeGroupsRules = False, orderByPriority = False,  includeDisabled = False, categoriesFilter = None, includeTriggerCategory = False):
		checkData(locals(), ["categoriesFilter"])
		if categoriesFilter: checkData(json.loads(categoriesFilter))

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		ruleList = []

		if username:
			from app.backend.model.user import User
			user = User(username = username)
			user.retrieve()
			ruleList = room.getRules( author = user, includeGroupsRules = includeGroupsRules, includeDisabled = includeDisabled, categoriesFilter = categoriesFilter)
		else:
			ruleList = room.getRules( includeGroupsRules = includeGroupsRules,  includeDisabled = includeDisabled , categoriesFilter = categoriesFilter)

		if orderByPriority:
			ruleList = sorted(ruleList, key=lambda rule: rule.getPriority(), reverse=True)

		response = []
		for rule in ruleList:

			ruleDict = rule.getDict(buildingName = buildingName, roomName = roomName)

			if includeTriggerCategory:
				from app.backend.controller.triggerManager import TriggerManager
				triggerManager = TriggerManager()
				triggers = triggerManager.translateTrigger(rule.antecedent)["triggers"]
				triggersCategory = []
				for trigger in triggers:
					if trigger["trigger"].category not in triggersCategory: triggersCategory.append(trigger["trigger"].category)
				ruleDict.update({'triggersCategory' : triggersCategory})

			response.append(ruleDict)

				

		return {"rules" : response}

	def getActiveRulesId(self, roomName, buildingName):
		checkData(locals(), ["categoriesFilter"])
	
		from app.backend.model.rules import Rules
		rules = Rules()
		return {"activeRules" : rules.getActiveRulesId(buildingName = buildingName, roomName = roomName)} 



	def getTriggers(self, roomName, buildingName):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		triggerList = room.getTriggers( )

		response = []
		for trigger in triggerList:
			response.append(trigger.getDict())
			

		return {"triggers" : response}

	def getActions(self, roomName, buildingName):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		actionList = room.getActions( )

		response = []
		for action in actionList:
			response.append(action.getDict())
			

		return {"actions" : response}


	def getUsers(self, roomName, buildingName):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		userList = room.getUsers( )

		response = []
		for user in userList:
			response.append(user.getDict())
			

		return {"users" : response}

	def getGroups(self, roomName, buildingName):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		groupList = room.getGroups( )

		response = []
		for group in groupList:
			response.append(group.getDict())
			

		return {"groups" : response}


	def bindTrigger(self):
		checkData(locals())

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : not yet implemented"

	def bindAction(self):
		checkData(locals())

		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : not yet implemented"

	def deleteRule(self, ruleId, buildingName, roomName, editorUuid):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		from app.backend.model.user import User
		editor = User(uuid = editorUuid)
		editor.retrieve()
		
		author = User(uuid = rule.authorUuid)
		author.retrieve()


		# If this room is not related to a room, I cannot modify it from this method
		if not rule.roomName:
			raise UserCredentialError("You cannot modify this group related rule.")

		# If this rule is not about this building
		if rule.buildingName != buildingName:
			raise UserCredentialError("You cannot modify the rule of another building.")			
			
		if author.uuid != editor.uuid:

			if not rule.groupId and not rule.getRoom().roomName in list(r.roomName for r in editor.getRooms()):
				raise UserCredentialError("You cannot modify a rule of a room you do not own.")				

			#if rule.getRoom() not in editor.getRooms():
			#	raise UserCredentialError("You cannot modify a rule of a room you do not own.")

			if rule.groupId:

				from app.backend.model.group import Group
				group = Group(buildingName = buildingName, id = groupId)
				group.retrieve()

				if not group:
					raise UserCredentialError("You cannot delete a rule of a room you do not own.")				

				if not group.crossRoomsValidation:
					raise UserCredentialError("You cannot delete a rule you do not own.")

				if not group.id in list(g.id for g in editor.getGroups()):
					raise UserCredentialError("You cannot delete a rule belonging to a group you do not own.")

				if not rule.getRoom().roomName in list(r.roomName for r in group.getRooms()):
					raise UserCredentialError("You cannot delete a rule belonging to room that does not belongs to a group you do not own.")

			if editor.level < rule.getPriority():
				raise UserCredentialError("You cannot modify this rule since it has a too high priority for your user level")			


		room.deleteRule(rule)

		return {}

	def disableRule(self, ruleId, buildingName, roomName, editorUuid):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		from app.backend.model.user import User
		editor = User(uuid = editorUuid)
		editor.retrieve()
		
		author = User(uuid = rule.authorUuid)
		author.retrieve()


		# If this room is not related to a room, I cannot modify it from this method
		if not rule.roomName:
			raise UserCredentialError("You cannot disable this group related rule.")

		# If this rule is not about this building
		if rule.buildingName != buildingName:
			raise UserCredentialError("You cannot disable the rule of another building.")			
			
		if author.uuid != editor.uuid:

			if not rule.groupId and not rule.getRoom().roomName in list(r.roomName for r in editor.getRooms()):
				raise UserCredentialError("You cannot disable a rule of a room you do not own.")				

			#if rule.getRoom() not in editor.getRooms():
			#	raise UserCredentialError("You cannot modify a rule of a room you do not own.")

			if rule.groupId:

				from app.backend.model.group import Group
				group = Group(buildingName = buildingName, id = groupId)
				group.retrieve()

				if not group:
					raise UserCredentialError("You cannot disable a rule of a room you do not own.")				

				if not group.crossRoomsValidation:
					raise UserCredentialError("You cannot disable a rule you do not own.")

				if not group.id in list(g.id for g in editor.getGroups()):
					raise UserCredentialError("You cannot disable a rule belonging to a group you do not own.")

				if not rule.getRoom().roomName in list(r.roomName for r in group.getRooms()):
					raise UserCredentialError("You cannot disable a rule belonging to room that does not belongs to a group you do not own.")

			if editor.level < rule.getPriority():
				raise UserCredentialError("You cannot modify this rule since it has a too high priority for your user levele")	

		room.disableRule(rule)

		return {}

	def enableRule(self, ruleId, buildingName, roomName, editorUuid):
		checkData(locals())

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId)
		rule.retrieve()

		return self.editRule(ruleId = rule.id, priority = rule.getPriority(), buildingName = buildingName,  roomName = roomName, 
					editorUuid = editorUuid, groupId = rule.groupId, ruleBody = None, 
					antecedent = rule.antecedent, consequent = rule.consequent, enabled = True)


	def getRuleInfo(self, buildingName = None, roomName = None, ruleId = None):
		checkData(locals())

		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, roomName = roomName)
		rule.retrieve()

		return rule.getDict(buildingName = None, roomName = None)


	def setRulePriority(self, buildingName, roomName, ruleId, rulePriority):
		checkData(locals())


		from app.backend.model.rule import Rule
		rule = Rule(id = ruleId, buildingName = buildingName, roomName = roomName)
		rule.retrieve()
		rule.setPriority(buildingName = buildingName, roomName = roomName, priority = rulePriority)

		return rule.getDict(buildingName = buildingName, roomName = roomName)


	def addRule(self, priority, buildingName, roomName, authorUuid, ruleBody):
		checkData(locals())

		return self.__addOrModifyRule(priority = priority, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, ruleBody = ruleBody)

	def editRule(self, ruleId, priority, buildingName, roomName, editorUuid, groupId, ruleBody = None, antecedent = None, consequent = None, enabled = True):
		checkData(locals())


		if not ruleBody:
			if not antecedent: raise MissingInputDataError("")
			if not consequent: raise MissingInputDataError("")

		if ruleBody and antecedent: raise TooManyInputParametersError("")
		if ruleBody and consequent: raise TooManyInputParametersError("")


		from app.backend.model.rule import Rule
		oldRule = Rule(id = ruleId)
		oldRule.retrieve()

		from app.backend.model.user import User
		author = User(uuid = oldRule.authorUuid)
		author.retrieve()

		editor = User(uuid = editorUuid)
		editor.retrieve()

		writePermission = False
		errorMessage = ""


		# If this room is not related to a room, I cannot modify it from this method
		if not oldRule.roomName:
			raise UserCredentialError("You cannot modify this group related rule.")

		# If this rule is not about this building
		if oldRule.buildingName != buildingName:
			raise UserCredentialError("You cannot modify the rule of another building.")			
			
		if author.uuid != editor.uuid:

			if not groupId and not oldRule.getRoom().roomName in list(r.roomName for r in editor.getRooms()):
				raise UserCredentialError("You cannot modify a rule of a room you do not own.")				

			#if oldRule.getRoom() not in editor.getRooms():
			#	raise UserCredentialError("You cannot modify a rule of a room you do not own.")

			if groupId:

				from app.backend.model.group import Group
				group = Group(buildingName = buildingName, id = groupId)
				group.retrieve()

				if not group:
					raise UserCredentialError("You cannot modify a rule of a room you do not own.")				

				if not group.crossRoomsValidation:
					raise UserCredentialError("You cannot modify a rule you do not own.")

				if not group.id in list(g.id for g in editor.getGroups()):
					raise UserCredentialError("You cannot modify a rule belonging to a group you do not own.")

				if not oldRule.getRoom().roomName in list(r.roomName for r in group.getRooms()):
					raise UserCredentialError("You cannot modify a rule belonging to room that does not belongs to a group you do not own.")

			if editor.level < oldRule.getPriority():
				raise UserCredentialError("You cannot modify this rule since it has a too high priority for your user level")			

		authorUuid = editorUuid	

		result = self.__addOrModifyRule(ruleId = ruleId, priority = priority, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, ruleBody = ruleBody, antecedent = antecedent, consequent = consequent, enabled = enabled)		

		from app.backend.controller.notificationsManager import NotificationsManager
		notifications = NotificationsManager()
		messageSubject = "Rule modified in building " + str(buildingName) + " room " + str(roomName)
		messageText = "The user " + str(editor.username) + " edited (or tried to edit) the rule <<" + str(oldRule.getFullRepresentation()) + ">>. The new rule is <<" + str(ruleBody) + ">>"
		notifications.sendNotification(buildingName = buildingName, roomName = roomName, messageSubject = messageSubject, messageText = messageText) 

		return result

	def __addOrModifyRule(self, priority = None, buildingName = None, roomName = None, authorUuid = None, ruleBody = None, ruleId = None, antecedent = None, consequent = None, enabled = True):
		checkData(locals())
		
		import time,datetime
		startTimeMilliseconds = long((time.time() + 0.5) * 1000)


		if ruleBody:
			try:
				antecedent = ruleBody.split("then")[0].replace("if ", "").strip()
				consequent = ruleBody.split("then")[1].strip()
			except Exception as e:
				raise NotWellFormedRuleError("There is a syntax error in the rule you are trying to save")

		
		# Detecting rule category (by the rule-consequent)
		from app.backend.controller.actionManager import ActionManager
		actionManager = ActionManager()
		category = actionManager.getAction(consequent).category
		
		from app.backend.model.user import User
		author = User(uuid = authorUuid)
		author.retrieve()

		if int(str(priority)) < 0 or int(str(priority)) > author.getMaxRoomPriority():
			raise RulePriorityError("You can specify rules for rooms with a priority value between 0 and " + str(author.getMaxRoomPriority()) + ". You inserted " + str(priority))



		from app.backend.model.rule import Rule
		from app.backend.model.room import Room

		if not ruleId:
			rule = Rule(priority = priority, category = category, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, antecedent = antecedent, consequent = consequent, enabled = True)
		else:
			rule = Rule(id = ruleId)
			rule.retrieve()
			author = rule.getAuthor()

			
			rule.antecedent = antecedent
			rule.consequent = consequent
			rule.authorUuid = authorUuid
			rule.authorUuid = authorUuid	
			rule.enabled = enabled		

			editor = rule.getAuthor()

			if editor.level < rule.getPriority():
				raise UserCredentialError("You cannot modify this rule since it has a too high priority for your user level")

		room = Room(buildingName = buildingName, roomName = roomName)
		room.retrieve()

		if not ruleId and not rule.checkIfUnique():
			raise DuplicatedRuleError("The submitted rule is already been saved for the considered room.")

		# excludedRuleId is needed to ignore the rule that the user want to edit
		excludedRuleId = ruleId if ruleId else None		

		roomRules = room.getRules(author = False, includeGroupsRules = True, excludedRuleId = excludedRuleId)

		# Checking that a priority is unique over the same category	
		for r in roomRules:
			if str(r.category) == str(category) and int(r.getPriority()) == int(priority):
				raise AlredyAssignedPriorityError("In room " + roomName + " the priority " + str(priority) + " has alredy been assigned to another rule with the same category!")

		temporaryRuleSet = []
		temporaryRuleSet.extend(roomRules)
		temporaryRuleSet.append(rule)

		#### OPTMIZATION ########################################################################################
		# Removing rules with a trigger that is different form the one of the rule I'm trying to insert or modify
		from app.backend.controller.triggerManager import TriggerManager
		triggerManager = TriggerManager()
		
		newRuleTriggers = triggerManager.translateTrigger(rule.antecedent)["triggers"]

		for i in range(0, len(temporaryRuleSet)):

			otherRuleTriggers = triggerManager.translateTrigger(temporaryRuleSet[i].antecedent)["triggers"]

			deleteRule = False

			if rule.category == temporaryRuleSet[i].category:
				for t1 in newRuleTriggers:
					for t2 in otherRuleTriggers:
						if t1 == t2:
							deleteRule = True
							break;
					if deleteRule: break;

			if deleteRule:
				del temporaryRuleSet[i]

		#### OPTMIZATION ########################################################################################


		for i in range(0, len(temporaryRuleSet)):
			temporaryRuleSet[i].groupId = None
			temporaryRuleSet[i].roomName = roomName


		from app.backend.controller.rulesetChecker import RulesetChecker
		rulesetChecker = RulesetChecker(temporaryRuleSet)
		ruleCheckErrorList = rulesetChecker.check()

		if len(ruleCheckErrorList) == 0:
			if ruleId: 
				rule.id = ruleId
				rule.setPriority(priority)


			from app.backend.commons.console import flash
			endTimeMilliseconds = long((time.time() + 0.5) * 1000)
			opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds
			flash("RoomRuleVerification [SUCCESS]: roomName = " + str(roomName) +" #rules=" + str(len(temporaryRuleSet)) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))


			return room.addRule(rule).getDict()
		else:
			from app.backend.commons.console import flash
			
			logMessage = "authorUuid =  " + str(authorUuid) + ", "
			logMessage += "buildingName =  " + str(buildingName) + ", "
			logMessage += "roomName =  " + str(roomName) + ", "
			logMessage += "ruleSetDescr =  " + str(temporaryRuleSet) + ", "
			logMessage += "newRule =  " + str(rule)

			flash("RuleValidationError: " + logMessage)

			endTimeMilliseconds = long((time.time() + 0.5) * 1000)
			opTimeMilliseconds = endTimeMilliseconds - startTimeMilliseconds
			flash("RoomRuleVerification [FAILED]: roomName = " + str(roomName) +" #rules=" + str(len(temporaryRuleSet)) + " - opTimeMilliseconds:" + str(opTimeMilliseconds))


			raise RuleValidationError(ruleCheckErrorList)

	def __str__(self):
		return "RoomsManager: "