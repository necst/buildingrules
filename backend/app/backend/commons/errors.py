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

class UserNotFoundError(Exception):
	pass

class BuildingNotFoundError(Exception):
	pass

class SessionNotFoundError(Exception):
	pass

class TriggerNotFoundError(Exception):
	pass

class ActionNotFoundError(Exception):
	pass

class ClassNotInitializedError(Exception):
	pass

class RuleNotFoundError(Exception):
	pass

class SessionCreationError(Exception):
	pass

class NotValidSessionError(Exception):
	pass

class SessionExpiredError(Exception):
	pass

class UserCredentialError(Exception):
	pass

class UnknownError(Exception):
	pass

class MissingInputDataError(Exception):
	pass

class IncorrectInputDataTypeError(Exception):
	pass

class UsernameNotAvailableError(Exception):
	pass

class UserBuildingBindingError(Exception):
	pass

class NotWellFormedRuleError(Exception):
	pass

class RuleValidationError(Exception):
	pass

class RuleValidationEngineError(Exception):
	pass

class DuplicatedRuleError(Exception):
	pass

class RuleInitFailedError(Exception):
	pass

class RoomRulePriorityNotFoundError(Exception):
	pass

class SessionNotFoundError(Exception):
	pass

class RulePriorityError(Exception):
	pass

class DriverNotFoundError(Exception):
	pass

class RuleTranslationNotFoundError(Exception):
	pass

class NewNotificationMissingInputError(Exception):
	pass

class WrongBuildingGroupRipartitionError(Exception):
	pass

class UnsupportedDriverParameterError(Exception):
	pass

class WeatherInfoError(Exception):
	pass

class TooManyInputParametersError(Exception):
	pass

class BuildingDepotError(Exception):
	pass

class AlredyAssignedPriorityError(Exception):
	pass

class BadInputError(Exception):
	pass

class SimulationModeNotSupportedError(Exception):
	pass
	
