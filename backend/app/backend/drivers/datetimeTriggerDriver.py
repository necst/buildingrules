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
import time

from app.backend.commons.errors import *
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver

class DatetimeTriggerDriver(GenericTriggerDriver):


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

	def __getIntFromDate(self, date):
		day = date[:date.find("/")]
		month = date[date.find("/")+1:]
		numericalDate =  int(str( time.strptime(day + " " + month + " 00", "%d %m %y").tm_yday ))

		return numericalDate

	def __getIntFromTime(self, time):
		pm = False
		if "PM" in time.upper():
			pm = True
		
		if "." in time or ":" in time:
			time = time.replace(":",".")
			time = time[:time.find(".")]
		
		time = int(time.replace("AM", "").replace("PM", "").replace("am", "").replace("pm", ""))
		if pm: time = int(time)+12
		
		return str(time)

	def __getIntFromDay(self, day):

		if day.upper().startswith("MON"): return str(1)
		if day.upper().startswith("TUE"): return str(2)
		if day.upper().startswith("WED"): return str(3)
		if day.upper().startswith("THU"): return str(4)
		if day.upper().startswith("FRI"): return str(5)
		if day.upper().startswith("SAT"): return str(6)
		if day.upper().startswith("SUN"): return str(7)


	def __simulatedEventTriggered(self):


		if self.parameters["operation"] == "DATE_IN_RANGE":

			par0 = self.__getIntFromDate(self.parameters['0'])
			par1 = self.__getIntFromDate(self.parameters['1'])
			today = self.__getIntFromDate(self.parameters["simulationParameters"]["date"])

			if today >= par0 and today <= par1:
				return True
			else:
				return False
			
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TIME_IN_RANGE":

			par0 = self.__getIntFromTime(self.parameters['0'])
			par1 = self.__getIntFromTime(self.parameters['1'])
			now = self.__getIntFromTime(self.parameters["simulationParameters"]["time"][:2])

			if now >= par0 and now <= par1:
				return True
			else:
				return False

			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TODAY":
			par0 = int(self.__getIntFromDay(self.parameters['0']))
			today = int(self.__getIntFromDay(self.parameters["simulationParameters"]["day"]))

			if today == par0:
				return True
			else:
				return False


		elif self.parameters["operation"] == "DAY_RANGE":
			par0 = int(self.__getIntFromDay(self.parameters['0']))
			par1 = int(self.__getIntFromDay(self.parameters['1']))
			
			today = int(self.__getIntFromDay(self.parameters["simulationParameters"]["day"]))

			if (today >= par0) and (today <= par1):
				return True
			else:
				return False


		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])

	def __actualEventTriggered(self):

		if self.parameters["operation"] == "DATE_IN_RANGE":

			par0 = self.__getIntFromDate(self.parameters['0'])
			par1 = self.__getIntFromDate(self.parameters['1'])
			today = self.__getIntFromDate(str((time.strftime("%d/%m"))))

			if today >= par0 and today <= par1:
				return True
			else:
				return False
			
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TIME_IN_RANGE":

			par0 = self.__getIntFromTime(self.parameters['0'])
			par1 = self.__getIntFromTime(self.parameters['1'])
			now = self.__getIntFromTime((time.strftime("%H")))

			if now >= par0 and now <= par1:
				return True
			else:
				return False

			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TODAY":
			par0 = int(self.__getIntFromDay(self.parameters['0']))
			today = int(datetime.datetime.today().weekday() + 1)

			if today == par0:
				return True
			else:
				return False


		elif self.parameters["operation"] == "DAY_RANGE":
			par0 = int(self.__getIntFromDay(self.parameters['0']))
			par1 = int(self.__getIntFromDay(self.parameters['1']))
			
			today = int(datetime.datetime.today().weekday() + 1)

			if (today >= par0) and (today <= par1):
				return True
			else:
				return False


		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])

	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()


	def eventTriggered(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()


	def __str__(self):
		return "DatetimeTriggerDriver: "