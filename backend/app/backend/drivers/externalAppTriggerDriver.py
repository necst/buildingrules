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
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class ExternalAppTriggerDriver(GenericTriggerDriver):


	# parameters = {}

	# parameters["operation"] = "AFTER"
	# parameters["val_0"] = 

	# parameters["operation"] = "BEFORE"
	# parameters["val_0"] = 

	# parameters["operation"] = "IN_RANGE"
	# parameters["val_0"] = 
	# parameters["val_1"] = 

	def __init__(self, parameters):
		self.parameters = parameters

	def __actualEventTriggered(self):
		import random

		if self.parameters["operation"] == "CALENDAR_MEETING":
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "DEMANDE_REPONSE":
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))

		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedEventTriggered(self):
		print "SimulationModeNotSupportedError"
		raise SimulationModeNotSupportedError()

	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()

	def eventTriggered(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()

	def __str__(self):
		return "ExternalAppTriggerDriver: "