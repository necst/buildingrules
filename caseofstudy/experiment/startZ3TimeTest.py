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
import sys
import subprocess
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from database import Database
import rest
import math

sessionKey = None
userUuid = None
username = "admin"
password = "brulesAdmin2014"


def start():

	global sessionKey
	global userUuid
	global username
	global password

	response = rest.request("/api/test", {'username' : username, 'password' : password})

start()
