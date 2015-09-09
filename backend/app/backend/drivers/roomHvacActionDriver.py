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

class RoomHvacActionDriver(GenericActionDriver):


	# parameters = {}

	# parameters["operation"] = "LIGHT_ON"
	# parameters["operation"] = "LIGHT_OFF"

	def __init__(self, parameters):
		self.parameters = parameters

	def __actualActuation(self):

		if self.parameters["operation"] == "HVAC_ON":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "HVAC_OFF":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "SET_TEMPERATURE":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "SET_HUMIDITY":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "HEATING_ON":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "HEATING_OFF":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "AIR_CONDITIONING_ON":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"

		elif self.parameters["operation"] == "AIR_CONDITIONING_OFF":		
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"


		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedActuation(self):


		if self.parameters["operation"] == "HVAC_ON":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "HVAC", actionTargetStatus = "ON")

		elif self.parameters["operation"] == "HVAC_OFF":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "HVAC", actionTargetStatus = "OFF")

		elif self.parameters["operation"] == "SET_TEMPERATURE":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "TEMPERATURE", actionTargetStatus = self.parameters["0"] + "-" + self.parameters["1"])

		elif self.parameters["operation"] == "SET_HUMIDITY":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "HUMIDITY", actionTargetStatus = self.parameters["0"] + "-" + self.parameters["1"])

		elif self.parameters["operation"] == "HEATING_ON":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "HEATING", actionTargetStatus = "ON")

		elif self.parameters["operation"] == "HEATING_OFF":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "HEATING", actionTargetStatus = "OFF")

		elif self.parameters["operation"] == "AIR_CONDITIONING_ON":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "AIR_CONDITIONING", actionTargetStatus = "ON")

		elif self.parameters["operation"] == "AIR_CONDITIONING_OFF":		
			writeSimulationLog(simulationParameters = self.parameters["simulationParameters"], actionTargetName = "AIR_CONDITIONING", actionTargetStatus = "OFF")

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


	

	



