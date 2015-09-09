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

class AppliancesNetwork:
	def __init__(self):
		pass

	def resetNetwork(self):

		database = Database()
		database.open()
		database.executeWriteQuery("TRUNCATE TABLE appliances_network;")
		database.close()



	def __str__(self):
		return "AppliancesNetwork "

