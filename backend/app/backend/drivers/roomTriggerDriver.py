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
import signal
import os.path
import httplib2
import urllib
import os

#ob-ucsd-cse.ucsd.edu:8000/dataservice/
#sensor_type = 'Zone Temperature'
#zone = 'RM-B200B'
#BD api key: 7d0a9b2f-11bd-40da-8ff5-f7836fe468c3
#auth_token: 1

from app.backend.commons.errors import *
from app.backend.commons.simulation import getSimulationValue
from app.backend.drivers.genericTriggerDriver import GenericTriggerDriver


class RoomTriggerDriver(GenericTriggerDriver):


	# parameters = {}

	# parameters["operation"] = "AFTER"
	# parameters["val_0"] = 

	def __init__(self, parameters):
		self.parameters = parameters
		self.api_key = '7d0a9b2f-11bd-40da-8ff5-f7836fe468c3';
		self.auth_token = '1';
		self.http = httplib2.Http()

	
	def __actualEventTriggered(self):

		import random

		if self.parameters["operation"] == "CHECK_PRESENCE":
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))


		elif self.parameters["operation"] == "CHECK_ABSENCE":
			
			print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ")  to be implemented"
			return bool(random.getrandbits(1))

		elif self.parameters["operation"] == "TEMPERATURE_IN_RANGE":


			try:
				buildingName = self.parameters["buildingName"]
				roomName = self.parameters["roomName"]
			except:
				raise MissingInputDataError("BuildingName and roomName are needed to check the temperature")
			
			currentScale = "F"
			sensor_uuid = self.get_uuid_from_context('Zone Temperature', roomName)
			temperature = self.read_present_value_by_uuid(sensor_uuid)

			temperature = float(temperature)

			if temperature >= float(self.parameters['0'].upper().replace(currentScale, "").strip()) and temperature <= float(self.parameters['1'].upper().replace(currentScale, "").strip()):
				return True
			else:
				return False
			

		
		else:
			raise UnsupportedDriverParameterError(self.parameters["operation"])


	def __simulatedEventTriggered(self):

		if self.parameters["operation"] == "CHECK_PRESENCE":
			
			if self.parameters["simulationParameters"]["occupancy"]:
				return bool(self.parameters["simulationParameters"]["occupancy"])
			else:
				return getSimulationValue("occupancy", self.parameters["simulationParameters"]["time"], None)


		elif self.parameters["operation"] == "CHECK_ABSENCE":
			
			
			if self.parameters["simulationParameters"]["occupancy"]:
				return not bool(self.parameters["simulationParameters"]["occupancy"])
			else:
				return not getSimulationValue("occupancy", self.parameters["simulationParameters"]["time"], None)
			

		elif self.parameters["operation"] == "TEMPERATURE_IN_RANGE":
		
			currentScale = "F"

			if self.parameters["simulationParameters"]["roomTemperature"]:
				temperature = float(self.parameters["simulationParameters"]["roomTemperature"].replace(currentScale, "").strip())
			else:
				temperature = getSimulationValue("roomTemperature", self.parameters["simulationParameters"]["time"], None)

			if temperature >= float(self.parameters['0'].upper().replace(currentScale, "").strip()) and temperature <= float(self.parameters['1'].upper().replace(currentScale, "").strip()):
				return True
			else:
				return False



	def get_uuid_from_context(self, sensor_type, zone):
	    try:
	        response = self.http.request(
	        "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/context/Type=" + sensor_type + "+Room=Rm-" + zone,
	        "GET",
	        headers={'content-type':'application/json', 'X-BD-Api-Key': self.api_key, 'X-BD-Auth-Token': self.auth_token}
	        )
	        #print "response: ", response

	    except Exception as e:
	        raise BuildingDepotError('Could not search by given context! ' + str(e))

	    response = response[1]
	    response_json = json.loads(response) 
	    sensors_list = response_json["sensors"]

	    try:
	        uuid = sensors_list[0]["uuid"]
	    except Exception as e: 
	        raise BuildingDepotError('Could not extract uuid out of response! ' + str(e) + " " + str(sensors_list))
	    
	    #print "Sensor uuid is " + uuid
	    
	    return uuid

	def read_present_value_by_uuid(self, sensor_uuid, sensorpoint_name = "PresentValue"):
	    url = "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/" + sensor_uuid + "/sensorpoints/" + sensorpoint_name + "/datapoints"

	    try:
	        response = self.http.request(
	        url,
	        "GET",
	        headers={"X-BD-Api-Key": self.api_key, "X-BD-Auth-Token": self.auth_token}
	        )
	        #print response
	        response_json = json.loads(response[1])
	        datapoints = response_json["datapoints"]
	        for time, data in datapoints[0].iteritems():
	            value = float(data)
	    except Exception as e:
	    	raise BuildingDepotError('Error, could not read present value! ' + str(e))

	    return value		

	def __simulatedEventTriggeredWrapper(self):
		print "[SIMULATION]" + "[" + self.parameters["simulationParameters"]["date"] + "]" + "[" + self.parameters["simulationParameters"]["time"] + "]", 
		return self.__simulatedEventTriggered()


	def eventTriggered(self):
		if 'simulationParameters' in self.parameters:
			return self.__simulatedEventTriggeredWrapper()
		return self.__actualEventTriggered()


	def __str__(self):
		return "RoomTriggerDriver: "

	    