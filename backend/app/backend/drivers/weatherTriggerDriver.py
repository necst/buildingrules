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
import urllib2

from app.backend.commons.errors import *
from app.backend.commons.simulation import getSimulationValue
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver


class WeatherTriggerDriver(GenericTriggerDriver):


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
		self.__WEATHER_SERVICE_FILE_PATH = "tools/weather/"

	def __actualEventTriggered(self):
	
		text = ""
		try:
			in_file = open(self.__WEATHER_SERVICE_FILE_PATH + "weather.json","r")
			text = in_file.read()
			in_file.close()			
		except:
			try:
				in_file = open(self.__WEATHER_SERVICE_FILE_PATH + "weather.json","r")
				text = in_file.read()
				in_file.close()
			except:
				raise WeatherInfoError("Impossible to retrieve weather information")

		weather = json.loads(text)


		if self.parameters["operation"] == "TEMPERATURE_IN_RANGE":

			currentScale = ""
			if 'C' in self.parameters['0'].upper(): 
				currentScale = 'C'
			elif 'F' in self.parameters['0'].upper(): 
				currentScale = 'F'
			else:
				raise WeatherInfoError("Unsupported temperature scale")
	
			kelvinTemp = float(weather["main"]["temp"])
			
			if currentScale == "F":
				convTemp = ((kelvinTemp - 273) * 1.8 ) + 32;
			elif currentScale == "C":
				convTemp = (kelvinTemp - 273);
			else:
				raise WeatherInfoError("Unsopported temperature scale parameter")
			
			if convTemp >= float(self.parameters['0'].upper().replace(currentScale, "").strip()) and convTemp <= float(self.parameters['1'].upper().replace(currentScale, "").strip()):
				return True
			else:
				return False

		elif self.parameters["operation"] == "CHECK_SUNNY":
			return True if weather["weather"][0]["main"].upper() == "CLEAR" else False

		elif self.parameters["operation"] == "CHECK_RAINY":
			return True if weather["weather"][0]["main"].upper() == "RAIN" else False

		elif self.parameters["operation"] == "CHECK_CLOUDY":
			return True if weather["weather"][0]["main"].upper() == "CLOUDS" else False


		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedEventTriggered(self):

		if self.parameters["operation"] == "TEMPERATURE_IN_RANGE":

			currentScale = "F"

			if self.parameters["simulationParameters"]["externalTemperature"]:
				convTemp = float(self.parameters["simulationParameters"]["externalTemperature"].replace(currentScale, "").strip())
			else:
				convTemp = getSimulationValue("externalTemperature", self.parameters["simulationParameters"]["time"], None)

			if convTemp >= float(self.parameters['0'].upper().replace(currentScale, "").strip()) and convTemp <= float(self.parameters['1'].upper().replace(currentScale, "").strip()):
				return True
			else:
				return False

		elif self.parameters["operation"] == "CHECK_SUNNY":

			if self.parameters["simulationParameters"]["weather"]:
				return True if self.parameters["simulationParameters"]["weather"].upper() == "SUNNY" else False
			else:
				return True if getSimulationValue("weather", self.parameters["simulationParameters"]["time"], None) == "SUNNY" else False


		elif self.parameters["operation"] == "CHECK_RAINY":
			if self.parameters["simulationParameters"]["weather"]:
				return True if self.parameters["simulationParameters"]["weather"].upper() == "RAINY" else False
			else:
				return True if getSimulationValue("weather", self.parameters["simulationParameters"]["time"], None) == "RAINY" else False

		elif self.parameters["operation"] == "CHECK_CLOUDY":
			if self.parameters["simulationParameters"]["weather"]:
				return True if self.parameters["simulationParameters"]["weather"].upper() == "CLOUDY" else False
			else:
				return True if getSimulationValue("weather", self.parameters["simulationParameters"]["time"], None) == "CLOUDY" else False



	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()
	

	def eventTriggered(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()

	def __str__(self):
		return "WeatherTriggerDriver: "