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

import json
import time
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify, Blueprint
import time
import datetime
import os

from app import app
import rest

from app.backend.controller.setupManager import SetupManager


gui = Blueprint('gui', __name__, template_folder='templates')

@gui.route('/')
def index():

	setupManager = SetupManager()
	setupManager.initializeNetwork("single_men")
	appliancesList = setupManager.getAppliancesList()

	return render_template('index.html', appliancesList = appliancesList)

def successResponse(response):

	if not response['request-success'] and response['request-errorName'] == 'SessionNotFoundError':
		flash("Your session is expired. Make a logout and then login again.")

	return response['request-success']	
