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

class Appliance:
	def __init__(self, id = None, name = None, label = None, brand = None, model = None, smartAppliance = None, protocol = None, address = None, timeslots = None):

		self.id = id
		self.name = name
		self.label = label
		self.brand = brand 							if brand else ""
		self.model = model							if model else ""
		self.smartAppliance = smartAppliance 		if smartAppliance else 0
		self.protocol = protocol					if protocol else ""
		self.address = address						if address else ""
		self.timeslots = timeslots 					if timeslots else {}

	def __replaceSqlQueryToken(self, queryTemplate):

		if self.id 				!= None	: 	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.name 			!= None	: 	queryTemplate = queryTemplate.replace("@@name@@", str(self.name))
		if self.label 			!= None	: 	queryTemplate = queryTemplate.replace("@@label@@", str(self.label))
		if self.brand 			!= None	: 	queryTemplate = queryTemplate.replace("@@brand@@", str(self.brand))
		if self.model 			!= None	: 	queryTemplate = queryTemplate.replace("@@model@@", str(self.model))
		if self.smartAppliance  != None	: 	queryTemplate = queryTemplate.replace("@@smart_appliance@@", str(int(self.smartAppliance)))
		if self.protocol 		!= None	: 	queryTemplate = queryTemplate.replace("@@protocol@@", str(self.protocol))
		if self.address 		!= None	: 	queryTemplate = queryTemplate.replace("@@address@@", str(self.address))
		if self.timeslots 		!= None	: 	queryTemplate = queryTemplate.replace("@@timeslots@@", str(json.dumps(self.timeslots, separators=(',',':'))))


		return queryTemplate

	def store(self):

		database = Database()
		database.open()

		if self.id:

			query = "SELECT COUNT(id) FROM appliances_network WHERE id = '@@id@@';"
			query = self.__replaceSqlQueryToken(query)
			queryResult = database.executeReadQuery(query)

			if int(queryResult[0][0]) > 0:
				query = "UPDATE appliances_network SET name = '@@name@@', label = '@@label@@', brand = '@@brand@@', model = '@@model@@', smart_appliance = '@@smart_appliance@@', protocol = '@@protocol@@', address = '@@address@@', timeslots = '@@timeslots@@' WHERE id = '@@id@@';"

		else:

			query = "SELECT COUNT(id) FROM appliances_network WHERE name = '@@name@@';"
			query = self.__replaceSqlQueryToken(query)
			queryResult = database.executeReadQuery(query)

			if int(queryResult[0][0]) > 0:
				query = "UPDATE appliances_network SET name = '@@name@@', label = '@@label@@', brand = '@@brand@@', model = '@@model@@', smart_appliance = '@@smart_appliance@@', protocol = '@@protocol@@', address = '@@address@@', timeslots = '@@timeslots@@' WHERE name = '@@name@@';"
			else:
				query = "INSERT INTO appliances_network (name, label, brand, model, smart_appliance, protocol, address, timeslots) VALUES ('@@name@@', '@@label@@', '@@brand@@', '@@model@@', '@@smart_appliance@@', '@@protocol@@', '@@address@@', '@@timeslots@@');"	
	
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		database.close()


	def retrieve(self):

		if self.id:
			query = "SELECT * FROM appliances_network WHERE id = '@@id@@';"
		elif self.name:
			query = "SELECT * FROM appliances_network WHERE name = '@@name@@';"
		else:
			raise MissingInputDataError("Impossibile to query any appliance with missing parameters")
			

		database = Database()
		database.open()

		
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)


		if len(queryResult) > 0:

			self.id = queryResult[0][0]
			self.name = queryResult[0][1]
			self.label = queryResult[0][2]
			self.brand = queryResult[0][3]
			self.model = queryResult[0][4]
			self.smartAppliance = queryResult[0][5]
			self.protocol = queryResult[0][6]
			self.address = queryResult[0][7]
			self.timeslots = json.loads(queryResult[0][8]) if queryResult[0][8] else None

		else:
			database.close()
			raise ApplianceNotFoundError("Impossibile to find any action with the provided values")


		database.close()


	def delete(self):

		database = Database()
		database.open()

		query = "DELETE FROM appliances_network WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getDict(self):
		
		response = {}

		response["id"] = self.id
		response["name"] = self.name
		response["label"] = self.label
		response["brand"] = self.brand
		response["model"] = self.model
		response["smartAppliance"] = self.smartAppliance
		response["protocol"] = self.protocol
		response["address"] = self.address
		response["timeslots"] = self.timeslots

		return response	

	def __str__(self):
		return "Appliance " + str(json.dumps(self.getDict(), separators=(',',':')))

