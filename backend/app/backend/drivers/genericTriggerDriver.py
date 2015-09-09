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

from app.backend.commons.errors import *

class GenericTriggerDriver:

	def __init__(self, parameters):
		self.parameters = parameters

	def __simulatedEventTriggered(self):
		print "SimulationModeNotSupportedError"
		raise SimulationModeNotSupportedError()

	def __actualEventTriggered(self):
		pass

	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()

	def eventTriggered(self):

		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()

		return self.__actualEventTriggered()


	def __str__(self):
		return "TimeTriggerDriver: "