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
import random
import string
import datetime
import re

from app.backend.commons.errors import *
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.trigger import Trigger
from app.backend.model.triggers import Triggers

class TriggerManager:

	def __init__(self):
		pass

	def getInfo(self, triggerName):
		checkData(locals())

		trigger = Action(triggerName = triggerName)
		trigger.retrive()
		return trigger.getDict()


	def getTriggerAndTemplateAndParameterValues(self, ruleAntecedent):
		checkData(locals())

		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		for trigger in triggerList:
			
			# A trigger.ruleAntecedent is represented as set of templates models:
			# Example "template1 | template2 | template2"
			# Where each template can be like
			# "it is between %d AM and %d AM | it is between %d AM and %d PM | it is between %d PM and %d AM | it is between %d PM and %d PM"

			models = trigger.ruleAntecedent.split('|')

			for model in models:
				parameterNumber = model.count("@val")
				originalModel = model.strip()
				model = model.replace("@val","(.+)").strip()
	

				matchObj = re.match( model, ruleAntecedent, re.M|re.I)

				if matchObj:
					parameterValues = {}

					for i in range(0,parameterNumber):
						parameterValues[str(i)] = matchObj.group(i + 1)

					return (trigger, originalModel, parameterValues)

		raise NotWellFormedRuleError("Impossible to find any trigger corresponding to the following rule consequent > " + ruleAntecedent)


	def getTriggerAndTemplate(self, ruleAntecedent):
		checkData(locals())

		trigger, template, parameterValues = self.getTriggerAndTemplateAndParameterValues(ruleAntecedent)
		return (trigger, template)

	def getTrigger(self, ruleAntecedent):
		checkData(locals())

		trigger, template = self.getTriggerAndTemplate(ruleAntecedent)
		return trigger

	def __translateParameters(self, triggerCategory, parameterValue):

		value = parameterValue

		if triggerCategory == "TIME":
			
			pm = False
			if "PM" in value.upper():
				pm = True
			
			if "." in value or ":" in value:
				value = value.replace(":",".")
				value = value[:value.find(".")]
			
		
			value = value.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", "")
			if pm: value = int(value)+12
			
			return str(value)

		if triggerCategory == "DATE":
			import time
			day = value[:value.find("/")]
			month = value[value.find("/")+1:]
			return str( time.strptime(day + " " + month + " 00", "%d %m %y").tm_yday )

		if triggerCategory == "DAY":
			if value.upper().startswith("MON"): return str(1)
			if value.upper().startswith("TUE"): return str(2)
			if value.upper().startswith("WED"): return str(3)
			if value.upper().startswith("THU"): return str(4)
			if value.upper().startswith("FRI"): return str(5)
			if value.upper().startswith("SAT"): return str(6)
			if value.upper().startswith("SUN"): return str(7)
			raise NotWellFormedRuleError("Impossibile to understand the mentioned name of the week.")


		if triggerCategory == "ROOM_TEMPERATURE" or triggerCategory == "EXT_TEMPERATURE":
			return value.replace("C", "").replace("F", "")

		return value


	def translateTrigger(self, ruleAntecedent, getDict = False):
		checkData(locals())

		translatedTriggers = []
		ruleAntecedent = ruleAntecedent.split(",")

		for currentAntecedent in ruleAntecedent:

			currentAntecedent = currentAntecedent.strip()

			triggers = Triggers()
			trigger, originalTemplate, parameterValues = self.getTriggerAndTemplateAndParameterValues(currentAntecedent)
			translationTemplate = triggers.translateTemplate('Z3', originalTemplate)

			translatedParams = {}

			for key,value in parameterValues.iteritems():
				translatedParams[key] = self.__translateParameters(trigger.category, value)

			translation = translationTemplate
			for i in range(0,len(parameterValues.keys())):

				value = translatedParams[str(i)]
				translation = translation.replace("@val", value, 1)

			currentTrigger = {}
			currentTrigger["antecedent"] = currentAntecedent
			currentTrigger["translation"] = translation
			currentTrigger["trigger"] = trigger if not getDict else trigger.getDict()
			currentTrigger["parameterValues"] = parameterValues
			currentTrigger["translatedParams"] = translatedParams
			

			translatedTriggers.append(currentTrigger)

		translationTemplate = "(and @@first_arg@@ @@second_arg@@)"		
		translation = translatedTriggers[0]["translation"]
		
		for i in range(1,len(translatedTriggers)):
			translation = (translationTemplate.replace('@@first_arg@@', translation)).replace('@@second_arg@@', translatedTriggers[i]["translation"])

		result = {}
		result["translation"] = translation
		result["triggers"] = translatedTriggers

		return result


	def getTriggerCategories(self):
		checkData(locals())
		
		triggers = Triggers()
		triggerList = triggers.getAllTriggers()

		categories = []
		for trigger in triggerList:
			if trigger.category not in categories:
				categories.append(trigger.category)

		return categories


	def getTriggerDriver(self, trigger, parameters = None):
		checkData(locals())

		from app.backend.drivers.datetimeTriggerDriver import DatetimeTriggerDriver
		from app.backend.drivers.roomTriggerDriver import RoomTriggerDriver
		from app.backend.drivers.weatherTriggerDriver import WeatherTriggerDriver
		from app.backend.drivers.fakeTriggerDriver import FakeTriggerDriver
		from app.backend.drivers.externalAppTriggerDriver import ExternalAppTriggerDriver

		if not parameters:
			parameters = {}

		if trigger.triggerName == "OCCUPANCY_TRUE":
			parameters.update({'operation' : 'CHECK_PRESENCE'})
			return RoomTriggerDriver(parameters = parameters)

		if trigger.triggerName == "OCCUPANCY_FALSE":
			parameters.update({'operation' : 'CHECK_ABSENCE'})
			return  RoomTriggerDriver(parameters = parameters)

		if trigger.triggerName == "ROOM_TEMPERATURE_RANGE":
			parameters.update({'operation' : 'TEMPERATURE_IN_RANGE'})
			return  RoomTriggerDriver(parameters = parameters)

		if trigger.triggerName == "TIME_RANGE":
			parameters.update({'operation' : 'TIME_IN_RANGE'})
			return  DatetimeTriggerDriver(parameters = parameters)

		if trigger.triggerName == "DATE_RANGE":
			parameters.update({'operation' : 'DATE_IN_RANGE'})
			return  DatetimeTriggerDriver(parameters = parameters)

		if trigger.triggerName == "TODAY":
			parameters.update({'operation' : 'TODAY'})
			return  DatetimeTriggerDriver(parameters = parameters)

		if trigger.triggerName == "DAY_RANGE":
			parameters.update({'operation' : 'DAY_RANGE'})
			return  DatetimeTriggerDriver(parameters = parameters)

		if trigger.triggerName == "EXT_TEMPERATURE_RANGE":
			parameters.update({'operation' : 'TEMPERATURE_IN_RANGE'})
			return  WeatherTriggerDriver(parameters = parameters)

		if trigger.triggerName == "SUNNY":
			parameters.update({'operation' : 'CHECK_SUNNY'})
			return  WeatherTriggerDriver(parameters = parameters)

		if trigger.triggerName == "RAINY":
			parameters.update({'operation' : 'CHECK_RAINY'})
			return  WeatherTriggerDriver(parameters = parameters)

		if trigger.triggerName == "CLOUDY":
			parameters.update({'operation' : 'CHECK_CLOUDY'})
			return  WeatherTriggerDriver(parameters = parameters)

		if trigger.triggerName == "NO_RULE":
			parameters.update({'operation' : 'NO_RULE'})
			return  FakeTriggerDriver(parameters = parameters)

		if trigger.triggerName == "DEMANDE_REPONSE":
			parameters.update({'operation' : 'DEMANDE_REPONSE'})
			return  ExternalAppTriggerDriver(parameters = parameters)

		if trigger.triggerName == "CALENDAR_MEETING":
			parameters.update({'operation' : 'CALENDAR_MEETING'})
			return  ExternalAppTriggerDriver(parameters = parameters)

		raise DriverNotFoundError("Impossibile to find any driver for the trigger " + str(trigger))


	def __str__(self):
		return "ActionManager: "