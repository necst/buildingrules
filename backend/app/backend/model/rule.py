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
import datetime
from app.backend.commons.errors import *
from app.backend.commons.database import Database

class Rule:
	def __init__(self, id = None, priority = None, category = None, buildingName = None, groupId = None, roomName = None, 
				authorUuid = None, antecedent = None, consequent = None, enabled = False, deleted = False, creationTimestamp = None, lastEditTimestamp = None):

			self.id = id
			self.__priority = priority
			self.category = category
			self.buildingName = buildingName
			self.groupId = groupId
			self.roomName = roomName
			self.authorUuid = authorUuid
			self.antecedent = antecedent
			self.consequent = consequent
			self.enabled = enabled
			self.deleted = deleted
			self.creationTimestamp = creationTimestamp
			self.lastEditTimestamp = lastEditTimestamp

	def __repr__(self):
		return repr((self.getDict()))			

	def disable(self):
		if self.id:
			self.enabled = False
			self.store()

	def enable(self):
		if self.id:
			self.enabled = True
			self.store()

	def delete(self):
		if self.id:
			self.deleted = True
			self.store()

	def undoDelete(self):
		if self.id:
			self.deleted = False
			self.store()

	def getPriority(self, roomName = None, buildingName = None):

		from app.backend.model.rulePriority import RulePriority


		if self.groupId and not roomName:
			return self.__priority
		elif self.groupId and roomName and buildingName:
			try:
				rulePriority = RulePriority(buildingName = buildingName, roomName = roomName, ruleId = self.id)
				rulePriority.retrieve()
				return rulePriority.rulePriority
			except RoomRulePriorityNotFoundError as e:
				return self.__priority
		elif self.roomName:
			try: 
				rulePriority = RulePriority(buildingName = self.buildingName, roomName = self.roomName, ruleId = self.id)
				rulePriority.retrieve()			
				return rulePriority.rulePriority
			except Exception as e:
				return self.__priority
		else:
			raise RuleInitFailedError("Some parameters are missing")

	def setPriority(self, priority, roomName = None, buildingName = None):
	
		from app.backend.model.rulePriority import RulePriority

		if self.groupId and not roomName:
			self.__priority = priority
		elif self.groupId and roomName and buildingName:
			rulePriority = RulePriority(buildingName = buildingName, roomName = roomName, ruleId = self.id, rulePriority = priority)
			rulePriority.store()
		elif self.roomName:
			rulePriority = RulePriority(buildingName = self.buildingName, roomName = self.roomName, ruleId = self.id, rulePriority = priority)
			rulePriority.store()			
		else:
			raise RuleInitFailedError("Some parameters are missing")

	def getBuilding(self):
		from app.backend.model.building import Building

		building = Building(buildingName = self.buildingName)
		building.retrieve()
		return building

	def getGroup(self):
		from app.backend.model.group import Group
		group = Group(id = self.groupId, buildingName  = self.buildingName)
		group.retrieve()
		return group

	def getRoom(self):
		from app.backend.model.room import Room
		room = Room(roomName = self.roomName, buildingName = self.buildingName)
		room.retrieve()
		return room

	def getAuthor(self):		
		from app.backend.model.user import User
		author = User(uuid = self.authorUuid)
		author.retrieve()
		return author


	def __replaceSqlQueryToken(self, queryTemplate):
		if self.id					!= None	:	queryTemplate = queryTemplate.replace("@@id@@", str(self.id))
		if self.__priority			!= None	:	queryTemplate = queryTemplate.replace("@@priority@@", str(self.__priority))
		if self.category			!= None	:	queryTemplate = queryTemplate.replace("@@category@@", self.category)
		if self.buildingName		!= None	:	queryTemplate = queryTemplate.replace("@@building_name@@", self.buildingName)
		if self.authorUuid			!= None	:	queryTemplate = queryTemplate.replace("@@author_uuid@@", str(self.authorUuid))
		if self.antecedent			!= None	:	queryTemplate = queryTemplate.replace("@@antecedent@@", self.antecedent)
		if self.consequent			!= None	:	queryTemplate = queryTemplate.replace("@@consequent@@", self.consequent)
		if self.enabled				!= None	:	queryTemplate = queryTemplate.replace("@@enabled@@", str(int(self.enabled)))
		if self.deleted				!= None	:	queryTemplate = queryTemplate.replace("@@deleted@@", str(int(self.deleted)))
		if self.creationTimestamp	!= None	:	queryTemplate = queryTemplate.replace("@@creation_timestamp@@", self.creationTimestamp.strftime('%Y-%m-%d %H:%M:%S'))
		if self.lastEditTimestamp	!= None	:	queryTemplate = queryTemplate.replace("@@last_edit_timestamp@@", self.lastEditTimestamp.strftime('%Y-%m-%d %H:%M:%S'))


		groupId = str(self.groupId) if self.groupId else "-1"
		roomName = str(self.roomName) if self.roomName else "None"

		queryTemplate = queryTemplate.replace("@@group_id@@", groupId)
		queryTemplate = queryTemplate.replace("@@room_name@@", roomName)


		return queryTemplate

	def store(self):

		updateQuery = False

		database = Database()
		database.open()

		query = "SELECT COUNT(id) FROM rules WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if self.lastEditTimestamp == None:
			self.lastEditTimestamp =  datetime.datetime.now() 

		if self.creationTimestamp == None:
			self.creationTimestamp = datetime.datetime.now() 


		if int(queryResult[0][0]) > 0:
			
			self.lastEditTimestamp =  datetime.datetime.now() 

			query = """UPDATE rules SET 
					priority = '@@priority@@', category = '@@category@@', building_name = '@@building_name@@', group_id = '@@group_id@@', room_name = '@@room_name@@', 
					author_uuid = '@@author_uuid@@', antecedent = '@@antecedent@@', consequent = '@@consequent@@', enabled = '@@enabled@@', 
					deleted = '@@deleted@@', creation_timestamp = '@@creation_timestamp@@', last_edit_timestamp = '@@last_edit_timestamp@@'
					WHERE id = '@@id@@';"""
			updateQuery = True
			
		else:

			query = """INSERT INTO rules (priority, category, building_name, group_id, room_name, author_uuid, antecedent, 
					consequent, enabled, deleted, creation_timestamp, last_edit_timestamp) VALUES (
					'@@priority@@', '@@category@@', '@@building_name@@', '@@group_id@@', '@@room_name@@', '@@author_uuid@@', '@@antecedent@@', '@@consequent@@', '@@enabled@@', 
					'@@deleted@@', '@@creation_timestamp@@', '@@last_edit_timestamp@@');"""


		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)
		self.id = int(database.getLastInsertedId()) if not self.id else self.id
		database.close()

		if not self.groupId and not updateQuery:
			from app.backend.model.rulePriority import RulePriority
			rulePriority = RulePriority(buildingName = self.buildingName, roomName = self.roomName, ruleId = self.id, rulePriority = self.__priority)
			rulePriority.store()



	def retrieve(self):
		database = Database()
		database.open()

		query = "SELECT * FROM rules WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		

		if len(queryResult) > 0:

			self.id = queryResult[0][0]
			self.__priority = int(queryResult[0][1])
			self.category = queryResult[0][2]
			self.buildingName = queryResult[0][3]
			self.authorUuid = int(queryResult[0][6])
			self.antecedent = queryResult[0][7]
			self.consequent = queryResult[0][8]
			self.enabled = bool(int(queryResult[0][9]))
			self.deleted = bool(int(queryResult[0][10]))
			self.creationTimestamp = queryResult[0][11]
			self.lastEditTimestamp = queryResult[0][12]

			groupId = int(queryResult[0][4])
			roomName = queryResult[0][5]

			self.groupId = groupId if groupId != -1 else None
			self.roomName = roomName if roomName != "None" else None


		else:
			database.close()
			raise RuleNotFoundError("Impossibile to find any rule with the provided values")

		database.close()

	def checkIfUnique(self):
		
		if self.groupId:
			query = "SELECT count(id) FROM rules WHERE building_name = '@@building_name@@' AND group_id = '@@group_id@@' AND antecedent = '@@antecedent@@' AND consequent = '@@consequent@@';"
		elif self.roomName:
			query = "SELECT count(id) FROM rules WHERE building_name = '@@building_name@@' AND room_name = '@@room_name@@' AND antecedent = '@@antecedent@@' AND consequent = '@@consequent@@';"
		else:
			raise MissingInputDataError("To check if a rule is unique, or groupId or roomName is needed.")	

		database = Database()
		database.open()		
		query = self.__replaceSqlQueryToken(query)
		queryResult = database.executeReadQuery(query)

		if int(queryResult[0][0]) > 0:
			return False

		return True



	def delete(self):
		print "\t\t\t\t\t\t\t\tTODO (" + self.__class__.__name__ + ":" + sys._getframe().f_code.co_name + ") : Consistency check not performed - Rule class"

		database = Database()
		database.open()

		query = "DELETE FROM rules WHERE id = '@@id@@';"
		query = self.__replaceSqlQueryToken(query)
		database.executeWriteQuery(query)

		database.close()

	def getFullRepresentation(self):
		return "if " + self.antecedent + " then " + self.consequent

	def getDict(self, roomName = None, buildingName = None):
	
		response = {}

		response["id"] = self.id
		response["priority"] = self.getPriority(roomName = roomName, buildingName = buildingName)
		response["category"] = self.category
		response["buildingName"] = self.buildingName
		response["groupId"] = self.groupId
		response["roomName"] = self.roomName
		response["authorUuid"] = self.authorUuid
		response["antecedent"] = self.antecedent
		response["consequent"] = self.consequent
		response["enabled"] = self.enabled
		response["deleted"] = self.deleted
		response["creationTimestamp"] = self.creationTimestamp.strftime('%Y-%m-%d %H:%M:%S') if self.creationTimestamp else None
		response["lastEditTimestamp"] = self.lastEditTimestamp.strftime('%Y-%m-%d %H:%M:%S') if self.lastEditTimestamp else None

		return response	


	def __str__(self):

		return "Rule " + str(json.dumps(self.getDict(), separators=(',',':')))