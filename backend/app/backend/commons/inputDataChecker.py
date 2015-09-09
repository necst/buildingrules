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
from app.backend.commons.errors import *


def checkData(parameters, excludedParameters = []):

	if type(parameters) == list:

		for parVal in parameters:
			if (type(parVal) == str or type(parVal) == unicode) and  "'" in parVal: raise BadInputError()
			if (type(parVal) == str or type(parVal) == unicode) and  '"' in parVal: raise BadInputError()			

	else:

		if parameters:
			for parName in parameters.keys():
				if parName not in excludedParameters:
					if parName != "self":
						
						parVal = parameters[parName]

						if (type(parVal) == str or type(parVal) == unicode) and  "'" in parameters[parName]: raise BadInputError()
						if (type(parVal) == str or type(parVal) == unicode) and  '"' in parameters[parName]: raise BadInputError()