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

from app import app
from app.backend.commons.test import Test

from app.backend.controller.usersManager import UsersManager
from app.backend.controller.sessionManager import SessionManager
from app.backend.controller.buildingsManager import BuildingsManager
from app.backend.controller.roomsManager import RoomsManager
from app.backend.controller.roomSimulator import RoomSimulator
from app.backend.controller.groupsManager import GroupsManager
from app.backend.controller.feedbackManager import FeedbackManager
from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager
from app.backend.controller.mTurkManager import MTurkManager

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/test', methods = ['GET', 'POST'])
def test():

	print "starting test 6..."
	test = Test()
	test.test6()
	#test.test2()
	#test.test3()
	#test.test0()

	return render_template('home.html')

@api.route('/api')
def index():
	return render_template('home.html')

@api.route('/api/users/<username>/login', methods = ['POST'])
def login(username = None):

	if request.method == 'POST':

		password = validateInput(request.form['password'])
		session = SessionManager()
		
		try:
			loginResult = session.login(username, password)	
			return returnResult( loginResult )

		except Exception as e:
			return returnError(e)
		

@api.route('/api/users/<username>/register', methods = ['POST'])
def register(username = None):

	if request.method == 'POST':

		password = validateInput(request.form['password'])
		personName = validateInput(request.form['personName'])
		email = validateInput(request.form['email'])
		
		usersManager = UsersManager()
		
		try:
			return returnResult( usersManager.registerTemporary(newUserUsername = username, newUserPassword = password, newUserEmail = email, newUserPersonName = personName) )

		except Exception as e:
			return returnError(e)
		

@api.route('/api/users/<username>/logout', methods = ['GET', 'POST'])
def logout(username = None):
	
	session = SessionManager()
	
	try:
		return returnResult(session.logout(username))

	except Exception as e:
		return returnError(e)

@api.route('/api/users/<username>', methods = ['POST'])
def userInfo(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			userManager = UsersManager()			
			return returnResult( userManager.getInfo(username = username) )		
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/mturk', methods = ['POST'])
def mturkInfo(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			mTurkManager = MTurkManager()			
			return returnResult( mTurkManager.getTodayToken(userUuid = userUuid) )		
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/feedbacks/store', methods = ['POST'])
def storeFeedback(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		authorUuid = userUuid
		alternativeContact = validateInput(request.form['alternativeContact'])		
		score = validateInput(request.form['score'])
		message = validateInput(request.form['message'])

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			feedbackManager = FeedbackManager()			
			return returnResult( feedbackManager.storeFeedback(authorUuid = authorUuid, alternativeContact = alternativeContact, score = score, message = message) )		
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/notifications', methods = ['POST'])
def userNotifications(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			from app.backend.controller.notificationsManager import NotificationsManager
			notifications = NotificationsManager()
			return returnResult( notifications.getNotifications(username = username, userUuid = userUuid) )		
		except Exception as e:
			return returnError(e)



@api.route('/api/users/<username>/rules/categories', methods = ['GET', 'POST'])
def ruleCategories(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			userManager = UsersManager()			

			from app.backend.controller.actionManager import ActionManager
			actionManager = ActionManager()
			categories = actionManager.getActionCategories()

			result = {"categories" : categories}

			return returnResult( result )		

		except Exception as e:
			return returnError(e)


@api.route('/api/users/uuid/<uuid>', methods = ['POST'])
def userInfoUuid(uuid = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			userManager = UsersManager()			
			return returnResult( userManager.getInfo(uuid = uuid) )		
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings', methods = ['POST'])
def userBuildings(username = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			userManager = UsersManager()
			return returnResult( userManager.getBuildingList(username) )		
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>', methods = ['POST'])
def buildingInfo(username = None, buildingName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			return returnResult( buildingsManager.getInfo(buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups', methods = ['POST'])
def buildingGroups(username = None, buildingName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			return returnResult( buildingsManager.getGroups(buildingName = buildingName, username = username) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>', methods = ['POST'])
def groupInfo(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.getInfo(groupId = groupId, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/delete', methods = ['POST'])
def deleteGroup(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			
			return returnResult( buildingsManager.deleteGroup(groupId = groupId, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms', methods = ['POST'])
def buildingRooms(username = None, buildingName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			return returnResult( buildingsManager.getRooms(buildingName = buildingName, username = username) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms', methods = ['POST'])
def groupRooms(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()
			return returnResult( groupsManager.getRooms(groupId = groupId, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/triggers', methods = ['POST'])
def getGroupTriggers(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()
			return returnResult( groupsManager.getTriggers(groupId = groupId, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/actions', methods = ['POST'])
def getGroupActions(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()
			return returnResult( groupsManager.getActions(groupId = groupId, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>', methods = ['POST'])
def roomInfo(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getInfo(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/simulation', methods = ['POST'])
def roomSimulation(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		
		occupancyTimeRangeFrom = validateInput(request.form['occupancyTimeRangeFrom'])	
		occupancyTimeRangeTo = validateInput(request.form['occupancyTimeRangeTo'])	
		roomTemperature = validateInput(request.form['roomTemperature'])	
		externalTemperature = validateInput(request.form['externalTemperature'])	
		weather = validateInput(request.form['weather'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomSimulator = RoomSimulator(buildingName = buildingName, roomName = roomName, occupancyTimeRangeFrom = occupancyTimeRangeFrom, occupancyTimeRangeTo = occupancyTimeRangeTo, roomTemperature = roomTemperature, externalTemperature = externalTemperature, weather = weather)

			return returnResult( roomSimulator.start() )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/activeRules', methods = ['POST'])
def roomActiveRules(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()
			return returnResult( roomsManager.getActiveRulesId(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/delete', methods = ['POST'])
def deleteRoom(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)

			return returnResult( buildingsManager.deleteRoom(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers', methods = ['POST'])
def roomTriggers(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getTriggers(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions', methods = ['POST'])
def roomActions(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getActions(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/users', methods = ['POST'])
def roomUsers(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getUsers(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/groups', methods = ['POST'])
def roomGroups(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getGroups(roomName = roomName, buildingName = buildingName) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules', methods = ['POST'])
def roomRules(username = None, buildingName = None, roomName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		
		filterByAuthor = getBoolFromString(validateInput(request.form['filterByAuthor'])) if 'filterByAuthor' in request.form.keys() else False
		includeGroupsRules = getBoolFromString(validateInput(request.form['includeGroupsRules'])) if 'includeGroupsRules' in request.form.keys() else False
		orderByPriority = getBoolFromString(validateInput(request.form['orderByPriority'])) if 'orderByPriority' in request.form.keys() else False
		includeTriggerCategory = getBoolFromString(validateInput(request.form['includeTriggerCategory'])) if 'includeTriggerCategory' in request.form.keys() else False
		
		try:
			categoriesFilter = request.form['categoriesFilter'] if 'categoriesFilter' in request.form.keys() else None
		except Exception as e:
			return returnError(e)
		

		usernameFilter = username if filterByAuthor else None

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getRules(roomName = roomName, buildingName = buildingName, username = usernameFilter, includeGroupsRules = includeGroupsRules, orderByPriority = orderByPriority, includeDisabled = True, categoriesFilter = categoriesFilter, includeTriggerCategory = includeTriggerCategory) )
		except Exception as e:
			return returnError(e)



@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/conflictingRules', methods = ['POST'])
def roomConflictingRules(username = None, buildingName = None, roomName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		
		ruleBody = validateInput(request.form['ruleBody'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getConflictingRules(roomName = roomName, buildingName = buildingName, ruleBody = ruleBody) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules', methods = ['POST'])
def groupRules(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.getRules(buildingName = buildingName, groupId = groupId) )
		except Exception as e:
			return returnError(e)
















@api.route('/api/users/<username>/register', methods = ['POST'])
def registerUser(username = None):
	
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		creatorUuid = userUuid
		newUserUsername = username
		newUserPassword = request.form['password']
		newUserEmail = request.form['email']
		newUserPersonName = request.form['personName']
		newUserLevel = request.form['level']

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			userManager = UsersManager()			
			return returnResult( userManager.register(creatorUuid, newUserUsername, newUserPassword, newUserEmail, newUserPersonName, newUserLevel) )		
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/add', methods = ['POST'])
def addRoomToBuilding(username = None, buildingName = None, roomName = None):

	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		description = validateInput(request.form['description'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
		
			return returnResult( buildingsManager.addRoom(roomName = roomName, buildingName = buildingName, description = description) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/add', methods = ['POST'])
def addRoomToGroup(username = None, buildingName = None, groupId = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()
			return returnResult( groupsManager.addRoom(groupId = groupId, buildingName = buildingName, roomName = roomName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/add', methods = ['POST'])
def addGroupToBuilding(username = None, buildingName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		description = validateInput(request.form['description'])	
		crossRoomsValidation = validateInput(request.form['crossRoomsValidation']) if 'crossRoomsValidation' in request.form.keys() else False							#BOOLEAN VALUE
		crossRoomsValidationCategories = request.form['crossRoomsValidationCategories']	if 'crossRoomsValidationCategories' in request.form.keys() else None	#LIST IN JSON FORMAT	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
		
			return returnResult( buildingsManager.addGroup(buildingName = buildingName, description = description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories) )
		except Exception as e:
			return returnError(e)			

@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/edit', methods = ['POST'])
def editGroupInBuilding(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		description = validateInput(request.form['description'])	
		crossRoomsValidation = validateInput(request.form['crossRoomsValidation']) if 'crossRoomsValidation' in request.form.keys() else False							#BOOLEAN VALUE
		crossRoomsValidationCategories = validateInput(request.form['crossRoomsValidationCategories'])	if 'crossRoomsValidationCategories' in request.form.keys() else None	#LIST IN JSON FORMAT		

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
		
			return returnResult( buildingsManager.editGroup(groupId = groupId, buildingName = buildingName, description = description, crossRoomsValidation = crossRoomsValidation, crossRoomsValidationCategories = crossRoomsValidationCategories) )
		except Exception as e:
			return returnError(e)



@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers/bind', methods = ['POST'])
def bindTriggerToRoom(username = None, buildingName = None, roomName = None):
	return render_template('home.html')	

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions/bind', methods = ['POST'])
def bindActionToRoom(username = None, buildingName = None, roomName = None):
	return render_template('home.html')	

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/add', methods = ['POST'])
def addRuleToRoom(username = None, buildingName = None, roomName = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		priority = validateInput(request.form['priority'])
		ruleBody = validateInput(request.form['ruleBody'])

		authorUuid = userUuid

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.addRule(priority = priority, buildingName = buildingName, roomName = roomName, authorUuid = authorUuid, ruleBody = ruleBody) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit', methods = ['POST'])
def editRuleInRoom(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		priority = validateInput(request.form['priority'])
		ruleBody = validateInput(request.form['ruleBody'])

		groupId = request.form['groupId'] if 'groupId' in request.form.keys() else None

		#authorUuid = userUuid
		editorUuid = userUuid

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.editRule(ruleId = ruleId, priority = priority, buildingName = buildingName, roomName = roomName, editorUuid = userUuid, ruleBody = ruleBody, groupId = groupId) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/setPriority', methods = ['POST'])
def setRulePriority(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		priority = validateInput(request.form['priority'])


		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()
			
			return returnResult( roomsManager.setRulePriority(buildingName = buildingName, roomName = roomName, ruleId = ruleId, rulePriority = priority) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>', methods = ['POST'])
def getRuleInfoFromRoom(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.getRuleInfo(ruleId = ruleId, buildingName = buildingName, roomName = roomName) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete', methods = ['POST'])
def deleteRuleInRoom(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.deleteRule(ruleId = ruleId, buildingName = buildingName, roomName = roomName, editorUuid = userUuid) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable', methods = ['POST'])
def disableRuleInRoom(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.disableRule(ruleId = ruleId, buildingName = buildingName, roomName = roomName, editorUuid = userUuid) )
		except Exception as e:
			return returnError(e)

@api.route('/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable', methods = ['POST'])
def enableRuleInRoom(username = None, buildingName = None, roomName = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			roomsManager = RoomsManager()

			return returnResult( roomsManager.enableRule(ruleId = ruleId, buildingName = buildingName, roomName = roomName, editorUuid = userUuid) )
		except Exception as e:
			return returnError(e)



@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/add', methods = ['POST'])
def addRuleToGroup(username = None, buildingName = None, groupId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		priority = validateInput(request.form['priority'])
		ruleBody = validateInput(request.form['ruleBody'])

		authorUuid = userUuid

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.addRule(priority = priority, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, ruleBody = ruleBody) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit', methods = ['POST'])
def editRuleInGroup(username = None, buildingName = None, groupId = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		priority = validateInput(request.form['priority'])
		ruleBody = validateInput(request.form['ruleBody'])

		authorUuid = userUuid

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.editRule(ruleId = ruleId, priority = priority, buildingName = buildingName, groupId = groupId, authorUuid = authorUuid, ruleBody = ruleBody) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>', methods = ['POST'])
def gerRuleInfoFromGroup(username = None, buildingName = None, groupId = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.getRuleInfo(ruleId = ruleId, buildingName = buildingName, groupId = groupId) )
		except Exception as e:
			return returnError(e)


@api.route('/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete', methods = ['POST'])
def deleteRuleInGroup(username = None, buildingName = None, groupId = None, ruleId = None):
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			buildingsManager = BuildingsManager()
			buildingsManager.checkUserBinding(buildingName, username)
			groupsManager = GroupsManager()

			return returnResult( groupsManager.deleteRule(ruleId = ruleId, buildingName = buildingName, groupId = groupId) )
		except Exception as e:
			return returnError(e)


@api.route('/api/tools/triggers/translate', methods = ['POST'])
def translateTrigger():
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		antecedent = validateInput(request.form['antecedent'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			triggerManager = TriggerManager()

			return returnResult( triggerManager.translateTrigger(ruleAntecedent = antecedent, getDict = True) )
		except Exception as e:
			return returnError(e)

@api.route('/api/tools/actions/translate', methods = ['POST'])
def translateAction():
	if request.method == 'POST':

		sessionKey = validateInput(request.form['sessionKey'])
		userUuid = validateInput(request.form['userUuid'])	
		consequent = validateInput(request.form['consequent'])	

		try:
			session = SessionManager()
			session.checkSessionValidity(sessionKey, userUuid)
			actionManager = ActionManager()

			return returnResult(actionManager.translateAction(ruleConsequent = consequent, getDict = True))
		except Exception as e:
			return returnError(e)			


def returnResult(result):


	result["request-error"] = False
	result["request-success"] = True
	jsonContent = jsonify(result)

	return jsonContent

def returnError(errorException):
	
	import logging

	response = {}
	response["request-success"] = False
	response["request-error"] = True
	response["request-errorName"] = errorException.__class__.__name__
	response["request-errorDescription"] = errorException.message

	jsonContent = jsonify(response)

	logging.exception("")

	return jsonContent


def getBoolFromString(stringValue):
	if stringValue.upper() == "TRUE": return True
	return False

def validateInput(formValue):
	if "'" in formValue or '"' in formValue:
		return ""

	return formValue
