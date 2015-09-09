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
from app.backend.commons.errors import *
from app.backend.commons.database import Database
from app.backend.model.building import Building

class Buildings:
	def __init__(self):
		pass

	def getAllBuildings(self):

		buildingList = []

		database = Database()
		query = "SELECT * FROM buildings;"
		database.open()
		queryResult = database.executeReadQuery(query)
		database.close()

		for record in queryResult:
			buildingName = record[0]
			label = record[1]
			description = record[2]

			building = Building(buildingName = buildingName, label = label, description = description)
			buildingList.append(building)

		
		return buildingList

	def __str__(self):
		return "Buildings: "