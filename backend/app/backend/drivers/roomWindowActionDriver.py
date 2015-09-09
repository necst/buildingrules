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

class RoomWindowActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def __actualActuation(self):

		if self.parameters["operation"] == "WINDOWS_OPEN":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "WINDOWS_CLOSE":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "CURTAINS_OPEN":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			
		elif self.parameters["operation"] == "CURTAINS_CLOSE":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "SET_BLIND":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"



		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedActuation(self):


		if self.parameters["operation"] == "WINDOWS_OPEN":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "WINDOWS", actionTargetStatus = "OPEN")

		elif self.parameters["operation"] == "WINDOWS_CLOSE":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "WINDOWS", actionTargetStatus = "CLOSE")

		elif self.parameters["operation"] == "CURTAINS_OPEN":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "CURTAINS", actionTargetStatus = "OPEN")
			
		elif self.parameters["operation"] == "CURTAINS_CLOSE":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "CURTAINS", actionTargetStatus = "CLOSE")

		elif self.parameters["operation"] == "SET_BLIND":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "BLIND", actionTargetStatus = self.parameters["0"])



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


	

	



