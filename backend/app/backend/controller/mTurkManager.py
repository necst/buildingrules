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
from app.backend.model.rules import Rules
from app.backend.model.mturk import Mturk
import time
import datetime
from datetime import timedelta


class MTurkManager:
	def __init__(self):
		pass

	def _getTokenFromDb(self, userUuid, day):
		mturk = Mturk(userUuid = userUuid, day = day)
		mturk.retrieve()
		return mturk.token

	def getTodayToken(self, userUuid):

		user = User(uuid = userUuid)
		user.retrieve()

		days = []
		for i in range(0,7):
			days.append( (user.registrationTimestamp + timedelta(days=i)).strftime("%Y-%m-%d"))
		
		today = str(time.strftime("%Y-%m-%d"))

		if today not in days:
			raise UnknownError("Today is not enabled for to use by the MTurk service. All the actions performed today will not be paid!")
		
		day = days.index(today)


		userRules = user.getCreatedRules()

		createdRulesCount = 0
		editedRulesCount = 0

		for rule in userRules:
			if str(rule.creationTimestamp).startswith(today): createdRulesCount += 1
			elif str(rule.lastEditTimestamp).startswith(today): editedRulesCount += 1

		userActionsCount = createdRulesCount + editedRulesCount

		result = {}

		requiredUserActions = [10, 8, 7, 5 , 4, 3, 2]
		#requiredUserActions = [2, 8, 7, 5 , 4, 3, 2]
		
		
		if userActionsCount >= requiredUserActions[day]:
			result["taskCompleted"] = True
			result["message"] = "You completed your today task!"
			result["token"] = self._getTokenFromDb(userUuid = userUuid, day = day)
		else:
			result["message"] = "You have still to perform " + str(requiredUserActions[day] - userActionsCount) + " actions on the rule sets!"
			result["taskCompleted"] = False
		
		result["currentDay"] = day + 1
		result["serverDatetime"] = str(time.strftime("%Y-%m-%d %H:%M:%S"))

		if day == 6 and result["taskCompleted"]:
			result["experimentCompleted"] = True
		else:
			result["experimentCompleted"] = False
 
		return {"mturk-status" : result}

		

	def __str__(self):
		return "MTurkManager: "