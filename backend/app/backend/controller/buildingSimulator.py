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
import time
import datetime
import copy
import os
import string
import random
from datetime import timedelta
import json

from app.backend.commons.inputDataChecker import checkData
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.roomSimulator import RoomSimulator

from datetime import datetime

class BuildingSimulator:

	def __init__(self, buildingName = None, startDate = None, numberOfDays = None, roomFilter = None):
		
		checkData(locals())

		self.buildingName = buildingName
		self.startDate = startDate
		self.numberOfDays = numberOfDays
		self.roomFilter = roomFilter

	def start(self):

		buildingsManager = BuildingsManager()

		days = []
		startDate = datetime.strptime(self.startDate, '%Y-%m-%d')
		for i in range(0, self.numberOfDays):
			days.append( (startDate + timedelta(days=i)).strftime("%Y-%m-%d"))


		for room in buildingsManager.getRooms(self.buildingName)["rooms"]:

			roomName = room["roomName"]

			if self.roomFilter:
				if not roomName in self.roomFilter:
					continue

			simulationResult = {}
			for day in days:

				roomSimulator = RoomSimulator(buildingName = self.buildingName, roomName = roomName, currentDate = day)
				simulationResult[day] = roomSimulator.start()

			if not os.path.exists("tools/simulation/results/"): os.makedirs("tools/simulation/results/")
			out_file = open("tools/simulation/results/" + roomName + ".json","w")
			out_file.write(json.dumps(simulationResult, separators=(',', ':')))
			out_file.close()


	def __str__(self):
		return "BuildingSimulator: "		



