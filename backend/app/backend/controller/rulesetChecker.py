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
import sys
import subprocess
import random
import string
from app.backend.commons.errors import *

from app.backend.model.rule import Rule
from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager


class RulesetChecker:

	def __init__(self, ruleList):
		self.ruleList = ruleList

		self.__MAIN_PATH = "tools/z3/"
		self.errorList = []


	def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def __addPrefixToFileName(self, filename):

		from hashlib import md5
		from time import localtime

		return "%s_%s_%s" % (self.__id_generator(), md5(str(localtime())).hexdigest(), filename)

	def check(self):

		triggerManager = TriggerManager()
		actionManager = ActionManager()
		assertionTemplate = "(assert (=> @@RULE_ANTECEDENT@@ @@RULE_CONSEQUENT@@))"
		finalAssertionTemplate = "(assert (and @@FIRST_ARG@@ @@SECOND_ARG@@ ))"
		rangeTriggersName = {"EXT_TEMPERATURE_RANGE" : "(extTempInRoom 1)", "ROOM_TEMPERATURE_RANGE" : "(tempInRoom 1)", "DATE_RANGE" : "(day 1)", "TIME_RANGE" : "(time 1)"}

		theoremBody = []
		theoremAssertions = []

		parametersIntervals = {}

		for rule in self.ruleList:

			translatedTriggers = triggerManager.translateTrigger(rule.antecedent) 
			translatedConsequent, action, parameters = actionManager.translateAction(rule.consequent)

			translatedAntecedent = translatedTriggers["translation"]

			currentRuleAssertion = assertionTemplate.replace("@@RULE_ANTECEDENT@@", translatedAntecedent)
			currentRuleAssertion = currentRuleAssertion.replace("@@RULE_CONSEQUENT@@",  translatedConsequent)

			# Adding the current rule to the theorem body
			theoremBody.append(currentRuleAssertion)

			# Now saving, in case of range based trigger, which intervals has to be checked
			for translatedTrigger in translatedTriggers["triggers"]:
				trigger = translatedTrigger["trigger"]
				parameters = translatedTrigger["translatedParams"]

				if trigger.triggerName in rangeTriggersName.keys():
					
					if trigger.triggerName not in parametersIntervals.keys():
						parametersIntervals[trigger.triggerName] = []
					
					parametersIntervals[trigger.triggerName].append(int(parameters['0']))
					parametersIntervals[trigger.triggerName].append(int(parameters['1']))
				
				else:
					theoremAssertions.append('(assert ' + translatedAntecedent + ')')


		for triggerName in parametersIntervals.keys():
			
			intervals = sorted(parametersIntervals[triggerName])

			#theoremAssertions.append('(assert (< ' + rangeTriggersName[triggerName] + ' '  + str(intervals[0]) + '))')
			for i in range(1, len(intervals)):
				firstArg = '(>= ' + rangeTriggersName[triggerName] + ' '  + str(intervals[i-1]) + ')'
				secondArg = '(<= ' + rangeTriggersName[triggerName] + ' '  + str(intervals[i]) + ')'
				theoremAssertions.append(finalAssertionTemplate.replace("@@FIRST_ARG@@", firstArg).replace("@@SECOND_ARG@@", secondArg))

			for i in intervals:
				theoremAssertions.append('(assert (= ' + rangeTriggersName[triggerName] + ' '  + str(i) + '))')				
			

		partialOutputFile = ""
		#File Header and Settings
		f = open(self.__MAIN_PATH + "header_template.txt")
		lines = f.readlines()
		f.close()
		for line in lines:
			partialOutputFile += line

		for assertion in theoremBody:
			partialOutputFile += assertion + "\n"

		for assertion in theoremAssertions:
			outputFile = partialOutputFile + assertion  + "\n"
			outputFile += "(check-sat)" + "\n"

			temporaryFilePath = self.__MAIN_PATH + self.__addPrefixToFileName("test_smt.z3")

			theOutFile = open(temporaryFilePath,"w")
			theOutFile.write(outputFile)
			theOutFile.close()	

			execStr = self.__MAIN_PATH + "z3/bin/z3 -smt2 " + temporaryFilePath
			#print execStr
			
			try:
				z3Output = subprocess.check_output(execStr, shell=True)
				os.remove(temporaryFilePath)
								
				if "unsat" in z3Output:
					error =  "There is a conflict in the rules! " + assertion
					print error
					self.errorList.append(error)
					return self.errorList
			except Exception as e :
				raise RuleValidationEngineError("The rule validation engine failed during rule checking.")


		return []


