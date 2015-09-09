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

from app.backend.commons.errors import *
from app.backend.commons.inputDataChecker import checkData
from app.backend.model.session import Session

class SessionManager:

	def __init__(self):
		pass

	def login(self, username, password):
		checkData(locals())

		if len(password) == 0 or len(username) == 0:
			raise MissingInputDataError("Insert username and password!")

		from app.backend.controller.usersManager import UsersManager

		usersManager = UsersManager()

		try:
			user = usersManager.getUser(username, password)
			sessionKey = self.__generateSessionKey()
			userUuid = user.uuid
			expireTimestamp = datetime.datetime.now() + datetime.timedelta(days=1)
			
			session = Session(sessionKey = sessionKey, userUuid = userUuid, expireTimestamp = expireTimestamp)
			
			try:
				session.store()
				sessionData = {"sessionKey" : sessionKey, "userUuid" : userUuid}
				return sessionData
			except SessionCreationError as e:
				raise e
			else:
				return None

		except UserNotFoundError as e:
			raise e
		else:
			return None
		
	def checkSessionValidity(self,sessionKey,userUuid):
		checkData(locals())

		session = Session(sessionKey = sessionKey, userUuid = userUuid)
		session.retrieve()

		try:
			session.retrieve()
		except SessionNotFoundError as e:
			raise NotValidSessionError("The requested session is not valid")
		except Exception as e:
			raise e

		if  datetime.datetime.now() > session.expireTimestamp:
			raise SessionExpiredError("The requested session is expired")

	def logout(self, username):
		checkData(locals())

		from app.backend.controller.usersManager import UsersManager
		usersManager = UsersManager()		
		user = usersManager.getUser(username)
		userUuid = user.uuid

		session = Session(userUuid = userUuid)
		session.retrieve()

		session.delete()

		return {}


	def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def __generateSessionKey(self):

		from hashlib import md5
		from time import localtime

		return "%s-%s" % (self.__id_generator(), md5(str(localtime())).hexdigest())


	def __str__(self):
		return "SessionManager: "