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
import sys
import time
import datetime
import json
import logging
import MySQLdb


def flash(message, color = None):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	
	messageSql = message.replace("'", '"')
	messageConsole = "BRules> " + str(st) + " > " + str(message)
	

	if color:
		if color == "red":
			messageConsole = '\033[1;31m' + messageConsole + '\033[1;m'
		elif color == "green":
			messageConsole =  '\033[1;32m' + messageConsole + '\033[1;m'
		elif color == "blue":
			messageConsole =  '\033[1;34m' + messageConsole + '\033[1;m'			
		elif color == "yellow":
			messageConsole =  '\033[1;33m' + messageConsole + '\033[1;m'									
		elif color == "gray":
			messageConsole =  '\033[1;30m' + messageConsole + '\033[1;m'			

	print messageConsole

	if len(messageSql.strip()):
		con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'buildingdepot', db = 'building_rules')
		cur = con.cursor()
		cur.execute("INSERT INTO `logs` (`logTimestamp`, `logMessage`) VALUES ('" + str(st) + "', '" + messageSql + "');")
		con.commit()
		con.close()