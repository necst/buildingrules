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
import os
import time
import datetime
import urllib2
import shutil
from app.backend.commons.console import flash

from app.backend.commons.errors import *

__SERVICE_FILE_PATH = "tools/weather/"

def start():
	flash("BuildingRules WeatherService is active...")
	while(1):
		try:
			main()
		except Exception as e:
			import logging
			logging.exception("")
			flash(e.message)

		time.sleep(600)
		

def main():

	flash("Updating weather informations...")

	restReadDone = False
	try:
		url = 'http://api.openweathermap.org/data/2.5/weather?q=LA,us'
		response = urllib2.urlopen(url).read()
		restReadDone = True
	except Exception as e:
		flash(e.message)

	if restReadDone:

		if not os.path.exists(__SERVICE_FILE_PATH):
			os.makedirs(__SERVICE_FILE_PATH)

		if os.path.exists(__SERVICE_FILE_PATH + "weather.json"):
			shutil.copy2(__SERVICE_FILE_PATH + "weather.json", __SERVICE_FILE_PATH + "weather.old.json")
		
		out_file = open(__SERVICE_FILE_PATH + "weather.json","w")
		out_file.write(response)
		out_file.close()
