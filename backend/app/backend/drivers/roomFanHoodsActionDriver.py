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
from app.backend.commons.simulation import writeSimulationLog
from app.backend.drivers.genericActionDriver import GenericActionDriver

class RoomFanHoodsActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def __actualActuation(self):

		if self.parameters["operation"] == "EXHAUST_FAN_ON":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			
		elif self.parameters["operation"] == "EXHAUST_FAN_OFF":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "FUME_HOODS_ON":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			
		elif self.parameters["operation"] == "FUME_HOODS_OFF":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])

	def __simulatedActuation(self):

		operation = self.parameters["operation"] 
		actionTargetName = operation[:operation.rfind("_")].strip()
		actionTargetStatus = operation[operation.rfind("_") + 1 :].strip()
		writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = actionTargetName, actionTargetStatus = actionTargetStatus)

	def __simulatedActuationWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		self.__simulatedActuation()

	def actuate(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedActuationWrapper()

		return self.__actualActuation()


	def __str__(self):
		return "RoomActionDriver: "


	

	



