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

gui = Blueprint('gui', __name__, template_folder='templates')

@gui.route('/')
def index():

	if loggedIn():
		return redirect(url_for('gui.buildings'))

	return render_template('home.html')

@gui.route('/partecipate/')
@gui.route('/partecipate')
def partecipate():
	return render_template('partecipate.html')

@gui.route('/mturkinfo/')
@gui.route('/mturkinfo')
def mturkinfo():
	return render_template('mturkinfo.html')


@gui.route('/userguide/')
@gui.route('/userguide')
def userguide():
	return render_template('userguide.html')



@gui.route('/login/', methods = ['GET', 'POST'])
@gui.route('/login', methods = ['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})

		if successResponse(response):
			session["logged_in"] = True
			session["sessionKey"] = response["sessionKey"]
			session["userUuid"] = response["userUuid"]
			session["username"] = username
			

			response = rest.request("/api/users/<username>", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
			if not successResponse(response): render_template('error.html', error = response['request-errorDescription'])
			session["userLevel"] = response["level"]
			session["userEmail"] = response["email"]
			session["maxRoomPriority"] = response["maxRoomPriority"]
			session["maxGroupPriority"] = response["maxGroupPriority"]

			response = rest.request("/api/users/<username>/buildings", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
			if not successResponse(response): render_template('error.html', error = response['request-errorDescription'])
			session["buildings"] = response["buildings"]

			return redirect(url_for('gui.index'))
		else:
			error = response['request-errorDescription']

	currentDatetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
	return render_template('login.html', error=error, currentDatetime = currentDatetime)	


@gui.route('/register/<source>', methods = ['GET', 'POST'])
@gui.route('/register/', methods = ['GET', 'POST'])
@gui.route('/register', methods = ['GET', 'POST'])
def register(source = None):
	error = None

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		personName = request.form['personName']
		email = request.form['email']

		response = rest.request("/api/users/<username>/register", {'username' : username, 'password' : password, 'personName' : personName, 'email' : email})

		if successResponse(response):

			userUuid = response["uuid"]

			return render_template('registrationOk.html', userUuid=userUuid)	
		else:
			error = response['request-errorDescription']

	return render_template('registerUser.html', error=error, source = source)	




@gui.route('/logout/')
@gui.route('/logout')
def logout():
	
	if loggedIn():

		response = rest.request("/api/users/<username>/logout", {'username' : session["username"]})

		del session["logged_in"]
		del session["sessionKey"]
		if "alreadyLoggedIn" in session.keys(): 
			del session["alreadyLoggedIn"]


		if successResponse(response):
			del session["userUuid"]
			del session["username"]
			del session["maxRoomPriority"]
			del session["maxGroupPriority"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])

	return render_template('home.html')	

@gui.route('/buildings/')
@gui.route('/buildings')
def buildings():

	if not loggedIn():	return redirect(url_for('gui.login'))
		
	response = rest.request("/api/users/<username>/buildings", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	if "buildings" not in response.keys():
		return render_template('error.html', error = response['request-errorDescription'])		

	if len(response["buildings"]) == 1:
		buildingName = response["buildings"][0]["buildingName"]
		return redirect(url_for('gui.buildingDetail', buildingName = buildingName))		

	return render_template('buildings.html', buildings = response["buildings"])	


	





@gui.route('/buildings/<buildingName>/')
@gui.route('/buildings/<buildingName>')
def buildingDetail(buildingName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if int(session["userLevel"]) < 100:
		return redirect(url_for('gui.rooms', buildingName = buildingName))
		
	response = rest.request("/api/users/<username>/buildings/<buildingName>", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if successResponse(response):
		return render_template('buildingInfo.html', buildingInfo = response)	
	else:
		return render_template('error.html', error = response['request-errorDescription'])


@gui.route('/buildings/<buildingName>/rooms/<roomName>/graphicalView/json/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/graphicalView/json', methods = ['GET', 'POST'])
def getGraphicalViewJson(buildingName = None, roomName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	username = session["username"]

	filePath = "tmp/gantt/json/" + username + "_" + buildingName + "_" + roomName + ".json"
	if not os.path.exists(filePath): return "[]"
	
	in_file = open(filePath,"r")
	text = in_file.read()
	in_file.close()	

	return text

@gui.route('/buildings/<buildingName>/rooms/<roomName>/graphicalView/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/graphicalView', methods = ['GET', 'POST'])
def roomGraphicalView(buildingName = None, roomName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	preloadGantt = False

	if getGraphicalViewJson(buildingName = buildingName, roomName = roomName) == "[]":
		preloadGantt = True

	ganttJsonLink = url_for("gui.getGraphicalViewJson", buildingName = buildingName, roomName = roomName)

	ganttView = []

	if request.method == 'POST':

		print request.form

		occupancyTimeRangeFrom = request.form['occupancyTimeRangeFrom']
		occupancyTimeRangeTo = request.form['occupancyTimeRangeTo']
		roomTemperature = request.form['roomTemperature']
		externalTemperature = request.form['externalTemperature']
		weather = request.form['weather']

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/simulation",
				{
					'username' : session["username"], 
					'buildingName' : buildingName,
					'sessionKey' : session["sessionKey"],
					'userUuid' : session["userUuid"],
					'roomName' : roomName,
					'occupancyTimeRangeFrom' : occupancyTimeRangeFrom,
					'occupancyTimeRangeTo' : occupancyTimeRangeTo,
					'roomTemperature' : roomTemperature,
					'externalTemperature' : externalTemperature,
					'weather' : weather
				})

		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		ganttBarColors = ['ganttRed', 'ganttGreen', 'ganttBlue', 'ganttOrange']
		currentBarColor = 0

		for target in response["simulation"].keys():

			item = {}
			item["name"] = target
			item["desc"] = ""
			item["values"] = []
			for bar in response["simulation"][target]:

				timeFrom = bar["from"].replace(".",":")
				timeTo = bar["to"].replace(".",":")

				today = datetime.date.today().strftime("%b %d %Y")
				unixTsFrom = EPOCH(today + " " + timeFrom)
				unixTsTo = EPOCH(today + " " + timeTo)

				unixTsFrom = str(int(unixTsFrom))
				unixTsTo = str(int(unixTsTo))

				item["values"].append({ "desc": bar["ruleText"],	"from" : "/Date(" + unixTsFrom + ")/", "to" : "/Date(" + unixTsTo + ")/", "label" : bar["status"], "customClass" : ganttBarColors[currentBarColor] })
				currentBarColor += 1
				if currentBarColor == len(ganttBarColors): currentBarColor = 0

			ganttView.append(item)


		username = session["username"]
		if not os.path.exists("tmp/gantt/json/"): os.makedirs("tmp/gantt/json/")
		out_file = open("tmp/gantt/json/" + username + "_" + buildingName + "_" + roomName + ".json","w")
		out_file.write(json.dumps(ganttView, separators=(',',':')))
		out_file.close()

	return render_template('gantt.html', ganttJsonLink = ganttJsonLink, preloadGantt = preloadGantt)			


@gui.route('/removeMe2/<currentDay>/', methods = ['GET', 'POST'])
@gui.route('/removeMe2/<currentDay>', methods = ['GET', 'POST'])
def removeMe2(currentDay = None):
	if not loggedIn():	return redirect(url_for('gui.login'))

	username = session["username"]

	filePath = "tmp/gantt/json/experiment_" + currentDay + ".json"
	if not os.path.exists(filePath): return "[]"
	
	in_file = open(filePath,"r")
	text = in_file.read()
	in_file.close()	

	return text



@gui.route('/removeMe/<currentDay>/', methods = ['GET', 'POST'])
@gui.route('/removeMe/<currentDay>', methods = ['GET', 'POST'])
def removeMe(currentDay = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	in_file = open("../backend/tools/simulation/results/3208.json","r")
	text = in_file.read()
	in_file.close()

	response = json.loads(text)

	for day in response.keys():
		print day

	ganttView = []
	ganttBarColors = ['ganttRed', 'ganttGreen', 'ganttBlue', 'ganttOrange']
	currentBarColor = 0

	print response[currentDay]

	for target in response[currentDay]["simulation"].keys():

		item = {}
		item["name"] = target
		item["desc"] = ""
		item["values"] = []
		for bar in response[currentDay]["simulation"][target]:

			timeFrom = bar["from"].replace(".",":")
			timeTo = bar["to"].replace(".",":")

			today = datetime.date.today().strftime("%b %d %Y")
			unixTsFrom = EPOCH(today + " " + timeFrom)
			unixTsTo = EPOCH(today + " " + timeTo)

			unixTsFrom = str(int(unixTsFrom))
			unixTsTo = str(int(unixTsTo))

			item["values"].append({ "desc": bar["ruleText"],	"from" : "/Date(" + unixTsFrom + ")/", "to" : "/Date(" + unixTsTo + ")/", "label" : bar["status"], "customClass" : ganttBarColors[currentBarColor] })
			currentBarColor += 1
			if currentBarColor == len(ganttBarColors): currentBarColor = 0

		ganttView.append(item)


	ganttJsonLink = url_for("gui.removeMe2", currentDay = currentDay)
	username = session["username"]
	if not os.path.exists("tmp/gantt/json/"): os.makedirs("tmp/gantt/json/")
	out_file = open("tmp/gantt/json/experiment_" + currentDay + ".json","w")
	out_file.write(json.dumps(ganttView, separators=(',',':')))
	out_file.close()

	return render_template('gantt2.html', ganttJsonLink = ganttJsonLink, preloadGantt = False)			


@gui.route('/buildings/<buildingName>/rooms/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms', methods = ['GET', 'POST'])
def rooms(buildingName = None):
	
	if not loggedIn():	return redirect(url_for('gui.login'))

	##################################
	# Retrieving the rules categories
	##################################
	response = rest.request("/api/users/<username>/rules/categories", {
		'username' : session["username"], 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})



	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	categories = response['categories']

	categoriesFilterList = []
	# CREATING THE LIST OF THE CHOSEN CATEGORIES
	for category in categories:
		currentKey = 'filter_by_' + category
		if currentKey in request.form.keys():
			if request.form[currentKey] == "True":
				categoriesFilterList.append(category)

	if len(categoriesFilterList) == 0:
		categoriesFilter = None
	else:
		categoriesFilter = json.dumps(categoriesFilterList, separators=(',',':'))
			
	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	notificationList = []
	roomList = response["rooms"]
	roomRules = {}
	authorList = {}
	groupList = {}
	triggerList = {}
	actionList = {}
	userList = {}
	roomGroupList = {}
	activeRoomRules = {}
	mTurkStatus = {}

	# Finding the map to show (remove me! - only for experiment) REMOVE ME REMOVE ME 
	mapFileName = "blankMap.png"
	for r in roomList:
		if r["description"] == "Office Room":
			mapFileName = r["roomName"] + ".png"
	# REMOVE ME REMOVE ME REMOVE ME REMOVE ME REMOVE ME REMOVE ME REMOVE ME 

	# Getting notifications
	response = rest.request("/api/users/<username>/notifications", 
		{
		'username' : session["username"],
		'sessionKey' : session["sessionKey"],
		'userUuid' : session["userUuid"]
		})

	if successResponse(response):
		notificationList = response["notifications"]
	else:
		return render_template('error.html', error = response['request-errorDescription'])

	mTurkStatus = None
	## Getting mTurk status
	#response = rest.request("/api/users/<username>/mturk", 
	#	{
	#	'username' : session["username"],
	#	'sessionKey' : session["sessionKey"],
	#	'userUuid' : session["userUuid"]
	#	})
	#
	#if successResponse(response):
	#	mTurkStatus = response["mturk-status"]
	#else:
	#	return render_template('error.html', error = response['request-errorDescription'])

	# Now retrieving room rules
	for room in roomList:
		roomName = room["roomName"]
		

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : True,
			'categoriesFilter' : categoriesFilter,
			'includeTriggerCategory' : True
			})

		if successResponse(response):
			roomRules[roomName] = response["rules"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/activeRules", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False
			})

		if successResponse(response):
			activeRoomRules[roomName] = response["activeRules"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/users", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			userList[roomName] = response["users"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/groups", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			roomGroupList[roomName] = response["groups"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			triggerList[roomName] = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			actionList[roomName] = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


			
		# Getting rules author uuid and groupId. I'll use them later
		for rule in roomRules[roomName]:
			if rule["authorUuid"] not in authorList.keys() and rule["authorUuid"] != session["userUuid"]:
				authorList[rule["authorUuid"]] = None
			if rule["groupId"] and rule["groupId"] not in groupList.keys():
				groupList[rule["groupId"]] = None


	# Getting user info per each stored uuid
	for authorUuid in authorList.keys():
		response = rest.request("/api/users/uuid/<uuid>", {'sessionKey' : session["sessionKey"], 'uuid' : authorUuid, 'userUuid' : session["userUuid"]})

		if successResponse(response):
			authorList[authorUuid] = response
		else:
			return render_template('error.html', error = response['request-errorDescription'])

	
	# Getting group info per each stored groupID
	for groupId in groupList.keys():
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>", {'username' : session["username"], 'buildingName' : buildingName, 'groupId' : groupId, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

		if successResponse(response):
			groupList[groupId] = response
		else:
			return render_template('error.html', error = response['request-errorDescription'])


	if "alreadyLoggedIn" in session.keys():
		alreadyLoggedIn = True
	else:
		session["alreadyLoggedIn"] = True
		alreadyLoggedIn = False

	return render_template('rooms.html', roomList = roomList, roomRules = roomRules, authorList = authorList, groupList = groupList, triggerList = triggerList, actionList = actionList, userList = userList, roomGroupList = roomGroupList, notificationList = notificationList, categories = categories, categoriesFilter = categoriesFilter, mapFileName = mapFileName, activeRoomRules = activeRoomRules, alreadyLoggedIn = alreadyLoggedIn, mTurkStatus = mTurkStatus)	


@gui.route('/buildings/<buildingName>/groups/')
@gui.route('/buildings/<buildingName>/groups')
def groups(buildingName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups", {
		'username' : session["username"], 
		'buildingName' : buildingName, 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	groupList = response["groups"]
	roomsGroup = {}
	rulesGroup = {}
	authorList = {}

	for group in groupList:

		# Getting the room list per each group
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'groupId' : group['id'],
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})


		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		if response["rooms"]:
			roomsGroup[group['id']] = response["rooms"]


		# Getting the rule list per each group
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'groupId' : group['id'],
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})


		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		if response["rules"]:
			rulesGroup[group['id']] = response["rules"]

			for rule in rulesGroup[group['id']]:
				if rule["authorUuid"] not in authorList.keys() and rule["authorUuid"] != session["userUuid"]:
					authorList[rule["authorUuid"]] = None

		# Getting user info per each stored uuid
		for authorUuid in authorList.keys():
			response = rest.request("/api/users/uuid/<uuid>", {'sessionKey' : session["sessionKey"], 'uuid' : authorUuid, 'userUuid' : session["userUuid"]})

			if successResponse(response):
				authorList[authorUuid] = response
			else:
				return render_template('error.html', error = response['request-errorDescription'])


	return render_template('groups.html', groupList = groupList, roomsGroup = roomsGroup, rulesGroup = rulesGroup, authorList = authorList)
		

@gui.route('/buildings/<buildingName>/groups/<groupId>/')
@gui.route('/buildings/<buildingName>/groups/<groupId>')
def groupDetail(buildingName = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")

	
	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>", {'groupId' : groupId, 'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
	if not successResponse(response): return render_template('error.html', error = response['request-errorDescription'])
	groupInfo = response

	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms", {'groupId' : groupId, 'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
	if not successResponse(response): return render_template('error.html', error = response['request-errorDescription'])
	rooms = response["rooms"]
	
	return render_template('groupInfo.html', groupInfo = groupInfo, rooms = rooms)	
		


@gui.route('/buildings/<buildingName>/groups/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/add', methods = ['GET', 'POST'])
def addGroup(buildingName = None):


	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	##################################
	# Retrieving the building roomList
	##################################
	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {
		'username' : session["username"], 
		'buildingName' : buildingName, 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])
	
	roomList = response["rooms"]


	##################################
	# Retrieving the rules categories
	##################################
	response = rest.request("/api/users/<username>/rules/categories", {
		'username' : session["username"], 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	categories = response['categories']


	##################################
	# Now manaing POST and GET requests
	##################################

	if request.method == 'GET':
		return render_template('groupForm.html', roomList = roomList, categories = categories)

	elif request.method == 'POST':

		description = request.form['description']
		crossRoomsValidation = request.form['crossRoomsValidation'] if 'crossRoomsValidation' in request.form.keys() else False
		crossRoomsValidationCategories = []


		# CREATING THE LIST OF THE CHOSEN CATEGORIES
		for category in categories:
			currentKey = 'filter_by_' + category
			if currentKey in request.form.keys():
				if request.form[currentKey] == "True":
					crossRoomsValidationCategories.append(category)

		# NOW STORING THE NEW GROUP
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/add", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'description' : description,
			'crossRoomsValidation' : crossRoomsValidation,
			'crossRoomsValidationCategories' : json.dumps(crossRoomsValidationCategories, separators=(',',':')),
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})

		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		# now let us add each selected room to the created group
		groupId = response['id']

		# NOW ADDING EACH SELECTED ROOM TO THE CREATED GROUP
		for room in roomList:

			if ("room_" + room["roomName"]) in request.form.keys():
				response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/add", {
					'username' : session["username"], 
					'buildingName' : buildingName, 
					'groupId' : groupId,
					'roomName' : room["roomName"],
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
				})

				if not successResponse(response):
					return render_template('error.html', error = response['request-errorDescription'])		


		return redirect(url_for('gui.groups', buildingName = buildingName))

	





@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/add', methods = ['GET', 'POST'])
def addRuleToRoom(buildingName = None, roomName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':

		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

		
		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/add", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})


		if successResponse(response):
			flash("The rule has been added correctly!")
			#return redirect(url_for('gui.rooms', buildingName = buildingName))
			return redirect('/buildings/' + buildingName + '/rooms' + '#roomMenu_' + roomName)
		else:
			print response

			if response["request-errorName"] == "RuleValidationError":
				return redirect(url_for('gui.addRuleToRoom', buildingName = buildingName, roomName = roomName, ruleBody = ruleBody, priority = priority, conflictFound = True))

			return render_template('error.html', error = response['request-errorDescription'], insertionForRoom = True)

	else:

		ruleBody = None
		priority = None
		conflictingRuleList = []
		conflictFound = request.args['conflictFound'] if 'conflictFound' in request.args.keys() else False
		
		if bool(conflictFound):

			ruleBody = request.args['ruleBody'].strip() if 'ruleBody' in request.args.keys() else None
			priority = request.args['priority'] if 'priority' in request.args.keys() else None

			response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/conflictingRules", 
				{
				'username' : session["username"],
				'buildingName' : buildingName, 
				'roomName' : roomName,
				'sessionKey' : session["sessionKey"],
				'userUuid' : session["userUuid"],
				'ruleBody' : ruleBody
				})

			if successResponse(response):
				conflictingRuleList = response["conflictingRules"]
			else:
				return render_template('error.html', error = response['request-errorDescription'])

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			triggerList = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			actionList = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		availableTriggers = []
		for trigger in triggerList:
			availableTriggers.append( trigger["ruleAntecedent"].split("@val")[0].strip() )


		availableActions = []
		for action in actionList:
			availableActions.append( action["ruleConsequent"].split("@val")[0].strip() )

		availableTriggers = sorted(availableTriggers)
		availableActions = sorted(availableActions)


		return render_template('ruleForm.html', insertionForRoom = True, availableTriggers = availableTriggers, availableActions = availableActions, ruleBody = ruleBody, priority = priority, conflictingRuleList = conflictingRuleList, conflictFound = conflictFound, roomName = roomName, buildingName = buildingName)	


@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/add', methods = ['GET', 'POST'])
def addRuleToGroup(buildingName = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	if request.method == 'POST':


		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

		
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/add", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})


		if successResponse(response):
			flash("The rule has been added correctly!")
			return redirect(url_for('gui.groups', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'])

	else:

		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'groupId' : groupId,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			print response
			triggerList = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'groupId' : groupId,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			actionList = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		availableTriggers = []
		for trigger in triggerList:
			availableTriggers.append( trigger["ruleAntecedent"].split("@val")[0].strip() )


		availableActions = []
		for action in actionList:
			availableActions.append( action["ruleConsequent"].split("@val")[0].strip() )

		availableTriggers = sorted(availableTriggers)
		availableActions = sorted(availableActions)


		return render_template('ruleForm.html', insertionForGroup = True,  availableTriggers = availableTriggers, availableActions = availableActions)	



@gui.route('/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
def editRoomRule(buildingName = None, roomName = None, ruleId = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':

		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

	
		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})
		
		
		if successResponse(response):
			flash("The rule has been saved correctly!")
			#return redirect(url_for('gui.rooms', buildingName = buildingName))
			return redirect('/buildings/' + buildingName + '/rooms' + '#roomMenu_' + roomName)
		else:

			if response["request-errorName"] == "RuleValidationError":
				return redirect(url_for('gui.editRoomRule', buildingName = buildingName, roomName = roomName, ruleId = ruleId, ruleBody = ruleBody, priority = priority, conflictFound = True))
			
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForRoom = True)

	else:


		conflictingRuleList = []
		conflictFound = request.args['conflictFound'] if 'conflictFound' in request.args.keys() else False
		
		if bool(conflictFound):

			ruleBody = request.args['ruleBody'] if 'ruleBody' in request.args.keys() else None
			priority = request.args['priority'] if 'priority' in request.args.keys() else None

			response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/conflictingRules", 
				{
				'username' : session["username"],
				'buildingName' : buildingName, 
				'roomName' : roomName,
				'sessionKey' : session["sessionKey"],
				'userUuid' : session["userUuid"],
				'ruleBody' : ruleBody
				})

			if successResponse(response):
				conflictingRuleList = response["conflictingRules"]
			else:
				return render_template('error.html', error = response['request-errorDescription'])


		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'ruleId' : ruleId,
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})

		if not successResponse(response):
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForRoom = True)

		rule = response

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			triggerList = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			actionList = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		availableTriggers = []
		for trigger in triggerList:
			availableTriggers.append( trigger["ruleAntecedent"].split("@val")[0].strip() )


		availableActions = []
		for action in actionList:
			availableActions.append( action["ruleConsequent"].split("@val")[0].strip() )

		availableTriggers = sorted(availableTriggers)
		availableActions = sorted(availableActions)

		return render_template('ruleForm.html', rule = rule, insertionForRoom = True, availableTriggers = availableTriggers, availableActions = availableActions, conflictingRuleList = conflictingRuleList, conflictFound = conflictFound, roomName = roomName, buildingName = buildingName)



@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable', methods = ['GET'])
def disableRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	#return redirect(url_for('gui.rooms', buildingName = buildingName))
	return redirect('/buildings/' + buildingName + '/rooms' + '#roomMenu_' + roomName)


@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable', methods = ['GET'])
def enableRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	#return redirect(url_for('gui.rooms', buildingName = buildingName))
	return redirect('/buildings/' + buildingName + '/rooms' + '#roomMenu_' + roomName)


@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete', methods = ['GET'])
def deleteRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	#return redirect(url_for('gui.rooms', buildingName = buildingName))
	return redirect('/buildings/' + buildingName + '/rooms' + '#roomMenu_' + roomName)




@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
def editGroupRule(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	if request.method == 'POST':

		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

	
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})
		
		
		if successResponse(response):
			flash("The rule has been saved correctly!")
			return redirect(url_for('gui.groups', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForGroup = True)

	else:

		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})

		if not successResponse(response):
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForGroup = True)

		rule = response

		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'groupId' : groupId,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			print response
			triggerList = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'groupId' : groupId,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"]
			})

		if successResponse(response):
			actionList = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		availableTriggers = []
		for trigger in triggerList:
			availableTriggers.append( trigger["ruleAntecedent"].split("@val")[0].strip() )


		availableActions = []
		for action in actionList:
			availableActions.append( action["ruleConsequent"].split("@val")[0].strip() )

		availableTriggers = sorted(availableTriggers)
		availableActions = sorted(availableActions)

		return render_template('ruleForm.html', rule = rule, insertionForGroup = True,availableTriggers = availableTriggers, availableActions = availableActions)





@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete', methods = ['GET'])
def deleteGroupRule(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'groupId' : groupId,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.groups', buildingName = buildingName))




@gui.route('/buildings/<buildingName>/groups/<groupId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/delete', methods = ['GET'])
def deleteGroup(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	if int(session["userLevel"]) < 100:
		return render_template('error.html', error = "You cannot enter this page.")


	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'groupId' : groupId,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.groups', buildingName = buildingName))



@gui.route('/feedbacks/send/', methods = ['POST'])
@gui.route('/feedbacks/send', methods = ['POST'])
def sendFeedback():

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':

		alternativeContact = request.form['alternativeContact']
		score = request.form['score']
		message = request.form['message']

		response = rest.request("/api/users/<username>/feedbacks/store", {
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"],
					'alternativeContact' : alternativeContact,
					'score' : score,
					'message' : message
					})

		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		flash("Thanks for your feedback!")

	return redirect(url_for('gui.index'))



def loggedIn():

	try:
		if "logged_in" in session.keys() and session["logged_in"]:
			return True
	except:
		pass

	return False


def successResponse(response):

	if not response['request-success'] and response['request-errorName'] == 'SessionNotFoundError':
		flash("Your session is expired. Make a logout and then login again.")

	return response['request-success']	


def EPOCH(utcDatetimeString):

	#Example: 'Jun 1 2005  1:33PM'

	
	from pytz import timezone
	import pytz
	import datetime

	timezoneCorretionDelta = datetime.timedelta(hours=1)
	utc_datetime = datetime.datetime.strptime(utcDatetimeString, '%b %d %Y %H:%M').replace(tzinfo=timezone('US/Pacific'))
	utc_datetime -= timezoneCorretionDelta

	UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, tzinfo = pytz.utc)
	delta = utc_datetime - UNIX_EPOCH
	seconds = delta.total_seconds()
	ms = seconds * 1000
	return ms


