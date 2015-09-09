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

class ApplianceNotFoundError(Exception):
	pass

class SettingNotFoundError(Exception):
	pass

class ClassNotInitializedError(Exception):
	pass

class NotValidFamilyProfileError(Exception):
	pass

class UnknownError(Exception):
	pass

class MissingInputDataError(Exception):
	pass

class IncorrectInputDataTypeError(Exception):
	pass

class TooManyInputParametersError(Exception):
	pass

class BadInputError(Exception):
	pass

class DefaultTimeSlotReadError(Exception):
	pass
	
