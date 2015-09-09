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


from app import app

def writeSimulationLog(simulationParameters, actionTargetName, actionTargetStatus):

	line = simulationParameters["date"] + ";" + simulationParameters["time"] + ";" + actionTargetName + ";" + str(actionTargetStatus) + ";" + str(simulationParameters["ruleId"]) + ";" + str(simulationParameters["ruleText"]) 
	open(simulationParameters["resultsBufferFile"],"a").write( line + "\n")



def getSimulationValue(category, timestamp, selectedFile = None):

	from random import randrange
	import os

	category = category.upper()

	if not selectedFile:
		fileFolder = "tools/simulation/data/"
		if category == "OCCUPANCY": fileFolder = fileFolder + "occupancy/"
		if category == "ROOMTEMPERATURE": fileFolder = fileFolder + "room_temperature/"
		if category == "EXTERNALTEMPERATURE": fileFolder = fileFolder + "external_temperature/"
		if category == "WEATHER": fileFolder = fileFolder + "weather/"

		availableLogs = len(filter(lambda x: not x.startswith("."), os.listdir(fileFolder)))

		currentFile = fileFolder + str(randrange(availableLogs)) + ".txt"
	else:
		currentFile = selectedFile

	f = open(currentFile)
	lines = f.readlines()
	f.close()

	timestamp = timestamp.replace(".",":").split(":") 
	timestampInt = int(timestamp[0]) * 60 + int(timestamp[1])	

	for line in lines:

		if ":" in line:
			currentTime = line.split("T")[1].split("-")[0]
			currentTime = currentTime.split(":")
			currenTimeInt = int(currentTime[0]) * 60 + int(currentTime[1])

			
	
			if currenTimeInt >= timestampInt: 

				value = line.split(",")[1]
				if category == "OCCUPANCY": return bool(value)
				if category == "ROOMTEMPERATURE": return float(value)
				if category == "EXTERNALTEMPERATURE": return float(value)
				if category == "WEATHER": 
					return value.strip().upper()

				
	

