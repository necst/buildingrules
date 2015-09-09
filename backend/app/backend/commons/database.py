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
import MySQLdb
import json

class Database:
	def __init__(self, host='localhost', user='root', pwd='buildingdepot', db='building_rules'):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db
		self.cur = None


	def open(self):
		self.con = MySQLdb.connect(
				host = self.host,
				user = self.user,
				passwd = self.pwd,
				db = self.db
				)

		self.cur = self.con.cursor()


	def close(self):
		return self.con.close()

	# for record in executeReadQuery(query): ...
	def executeReadQuery(self, query):
		self.cur.execute(query)
		return self.cur.fetchall()

	def executeWriteQuery(self, query):
		self.cur.execute(query)
		self.con.commit()	

	def getLastInsertedId(self):
		return self.cur.lastrowid
