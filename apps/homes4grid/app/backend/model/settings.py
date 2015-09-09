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
from app.backend.model.setting import Setting

class Settings:
	def __init__(self):
		pass

	def get(self, key):
		
		setting = Setting(key = key)
		setting.retrieve()
		return setting.value

	def set(self, key, value):

		setting = Setting(key = key, value = value)
		setting.store()

	def __str__(self):
		return "Settings"

