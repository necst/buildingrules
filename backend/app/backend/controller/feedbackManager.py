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
import random
import string
import datetime
import re

from app.backend.commons.errors import *
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.feedback import Feedback

class FeedbackManager:

	def __init__(self):
		pass

	def storeFeedback(self, authorUuid, alternativeContact = None, score = None, message = None):
		checkData(locals())

		feedback = Feedback(authorUuid = authorUuid, alternativeContact = alternativeContact, score = score, message = message)
		feedback.store()

		return feedback.getDict()


	def __str__(self):
		return "ActionManager: "