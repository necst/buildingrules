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
import datetime
import urllib2
import shutil
from app.backend.commons.console import flash

from app.backend.commons.errors import *

__SERVICE_FILE_PATH = "tools/dbDump/"

def start():
	flash("BuildingRules DatabaseDumper is active...")
	while(1):
		try:
			main()
		except Exception as e:
			import logging
			logging.exception("")
			flash(e.message)

		time.sleep(43200)
		

def main():

	flash("Dumping database...")

	
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
	fileName = "db_dump_" + st + ".sql"

	if not os.path.exists(__SERVICE_FILE_PATH):
		os.makedirs(__SERVICE_FILE_PATH)

	cmd = "mysqldump -u root -pbuildingdepot building_rules > " + __SERVICE_FILE_PATH + fileName
	
	flash(cmd)
	os.system(cmd)

