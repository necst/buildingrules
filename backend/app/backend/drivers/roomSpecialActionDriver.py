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

class RoomSpecialActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def __actualActuation(self):


		if self.parameters["operation"] == "SEND_COMPLAIN":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedActuation(self):


		if self.parameters["operation"] == "SEND_COMPLAIN":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "SEND_COMPLAIN", actionTargetStatus = "TRUE")
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "SEND_COMPLAIN", actionTargetStatus = "FALSE")
			
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedActuationWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		self.__simulatedActuation()

	def actuate(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedActuationWrapper()

		return self.__actualActuation()


	def __str__(self):
		return "RoomActionDriver: "


	

	



