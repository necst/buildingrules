# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.34-0ubuntu0.12.04.1)
# Database: building_rules
# Generation Time: 2014-02-22 02:42:42 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table actions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `actions`;

CREATE TABLE `actions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(24) DEFAULT NULL,
  `action_name` varchar(24) DEFAULT NULL,
  `rule_consequent` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;

INSERT INTO `actions` (`id`, `category`, `action_name`, `rule_consequent`, `description`)
VALUES
	(1,'LIGHT','LIGHT_ON','turn on the room light','turn on the room light'),
	(2,'LIGHT','LIGHT_OFF','turn off the room light','turn off the room light'),
	(3,'WINDOWS','WINDOWS_OPEN','open the windows','open the windows'),
	(4,'WINDOWS','WINDOWS_CLOSE','close the windows','close the windows'),
	(5,'HVAC','HVAC_ON','turn heating, ventilation and air conditioning on','turn heating, ventilation and air conditioning on'),
	(6,'HVAC','HVAC_OFF','turn heating, ventilation and air conditioning off','turn heating, ventilation and air conditioning off'),
	(7,'HVAC_TEMP','SET_TEMPERATURE','set temperature between @val and @val','set temperature'),
	(8,'HVAC_HUM','SET_HUMIDITY','set humidity between @val and @val','set humidity'),
	(9,'APP_COFFEE','COFFEE_ON','turn on the coffee machine','turn on the coffee machine'),
	(10,'APP_COFFEE','COFFEE_OFF','turn off the coffee machine','turn off the coffee machine'),
	(11,'APP_PRINTER','PRINTER_ON','turn on the printer','turn on the printer'),
	(12,'APP_PRINTER','PRINTER_OFF','turn off the printer','turn off the printer'),
	(13,'APP_COMPUTER','COMPUTER_ON','wake up my computer','wake up my computer'),
	(14,'APP_COMPUTER','COMPUTER_OFF','put to sleep my computer','put to sleep my computer'),
	(15,'APP_DESKLIGHT','DESKLIGHT_ON','turn on my desk light','turn on my desk light'),
	(16,'APP_DESKLIGHT','DESKLIGHT_OFF','turn off my desk light','turn off my desk light'),
	(17,'APP_DISPLAYMONITOR','DISPLAYMONITOR_ON','turn on display monitors','turn on display monitors'),
	(18,'APP_DISPLAYMONITOR','DISPLAYMONITOR_OFF','turn off display monitors','turn off display monitors'),
	(19,'SEND_COMPLAIN','SEND_COMPLAIN','send complain to building manger','send complain to building manger'),
	(20,'CURTAINS','CURTAINS_OPEN','open the curtains','open the curtains'),
	(21,'CURTAINS','CURTAINS_CLOSE','close the curtains','close the curtains'),
	(22,'APP_PROJECTOR','PROJECTOR_ON','turn on the projector','turn on the projector'),
	(23,'APP_PROJECTOR','PROJECTOR_OFF','turn off the projector','turn off the projector'),
	(24,'APP_AUDIO','AUDIO_ON','turn on the audio system','turn on the audio system'),
	(25,'APP_AUDIO','AUDIO_OFF','turn off the audio system','turn off the audio system'),
	(26,'EXHAUST_FAN','EXHAUST_FAN_ON','turn on the exhaust fan','turn on the exhaust fan'),
	(27,'EXHAUST_FAN','EXHAUST_FAN_OFF','turn off the exhaust fan','turn off the exhaust fan'),
	(28,'FUME_HOODS','FUME_HOODS_ON','turn on the fume hoods','turn on the fume hoods'),
	(29,'FUME_HOODS','FUME_HOODS_OFF','turn off the fume hoods','turn off the fume hoods'),
	(30,'BLIND','SET_BLIND','set blind to @val','set blind'),
	(31,'HEATING','HEATING_ON','turn on the heating','turn on the heating'),
	(32,'HEATING','HEATING_OFF','turn off the heating','turn off the heating'),
	(33,'AIR_CONDITIONING','AIR_CONDITIONING_ON','turn on the air conditioning','turn on the air conditioning'),
	(34,'AIR_CONDITIONING','AIR_CONDITIONING_OFF','turn off the air conditioning','turn off the air conditioning'),
	(35,'APP_MICROWAVE','APP_MICROWAVE_ON','turn on the microwave','turn on the microwave'),
	(36,'APP_MICROWAVE','APP_MICROWAVE_OFF','turn off the microwave','turn off the microwave');

/*!40000 ALTER TABLE `actions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table active_rules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `active_rules`;

CREATE TABLE `active_rules` (
  `building_name` varchar(11) DEFAULT NULL,
  `room_name` varchar(11) DEFAULT NULL,
  `rule_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table buildings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `buildings`;

CREATE TABLE `buildings` (
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `label` varchar(11) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `buildings` WRITE;
/*!40000 ALTER TABLE `buildings` DISABLE KEYS */;

INSERT INTO `buildings` (`building_name`, `label`, `description`)
VALUES
	('CSE','CSE','Computer Science Eng');

/*!40000 ALTER TABLE `buildings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table feedbacks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `feedbacks`;

CREATE TABLE `feedbacks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `author_uuid` int(11) DEFAULT NULL,
  `alternative_contact` varchar(64) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `message` longtext,
  `feedback_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `groups`;

CREATE TABLE `groups` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `description` longtext,
  `cross_rooms_validation` int(11) DEFAULT NULL,
  `cross_rooms_validation_categories` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`,`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `logs`;

CREATE TABLE `logs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `logTimestamp` timestamp NULL DEFAULT NULL,
  `logMessage` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table mturk
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mturk`;

CREATE TABLE `mturk` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` int(11) DEFAULT NULL,
  `user_uuid` int(11) DEFAULT NULL,
  `token` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table notifications
# ------------------------------------------------------------

DROP TABLE IF EXISTS `notifications`;

CREATE TABLE `notifications` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `send_timestamp` timestamp NULL DEFAULT NULL,
  `message_subject` varchar(128) DEFAULT NULL,
  `message_text` longtext,
  `recipient_uuid` int(11) DEFAULT NULL,
  `message_read` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table rooms
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `description` longtext,
  PRIMARY KEY (`room_name`,`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;

INSERT INTO `rooms` (`room_name`, `building_name`, `description`)
VALUES
	('100','CSE','Room');

/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms_actions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_actions`;

CREATE TABLE `rooms_actions` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `action_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms_actions` WRITE;
/*!40000 ALTER TABLE `rooms_actions` DISABLE KEYS */;

INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`)
VALUES
	('100','CSE',1),
	('100','CSE',2),
	('100','CSE',3),
	('100','CSE',4),
	('100','CSE',5),
	('100','CSE',6),
	('100','CSE',7),
	('100','CSE',8),
	('100','CSE',9),
	('100','CSE',10),
	('100','CSE',11),
	('100','CSE',12),
	('100','CSE',13),
	('100','CSE',14),
	('100','CSE',15),
	('100','CSE',16),
	('100','CSE',17),
	('100','CSE',18),
	('100','CSE',19),
	('100','CSE',20),
	('100','CSE',21),
	('100','CSE',22),
	('100','CSE',23),
	('100','CSE',24),
	('100','CSE',25),
	('100','CSE',26),
	('100','CSE',27),
	('100','CSE',28),
	('100','CSE',29),
	('100','CSE',30),
	('100','CSE',31),
	('100','CSE',32),
	('100','CSE',33),
	('100','CSE',34),
	('100','CSE',35),
	('100','CSE',36);

/*!40000 ALTER TABLE `rooms_actions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_groups`;

CREATE TABLE `rooms_groups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `room_name` varchar(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`group_id`,`building_name`,`room_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table rooms_triggers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_triggers`;

CREATE TABLE `rooms_triggers` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `trigger_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`trigger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms_triggers` WRITE;
/*!40000 ALTER TABLE `rooms_triggers` DISABLE KEYS */;

INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`)
VALUES
	('100','CSE',1),
	('100','CSE',2),
	('100','CSE',3),
	('100','CSE',4),
	('100','CSE',5),
	('100','CSE',6),
	('100','CSE',7),
	('100','CSE',8),
	('100','CSE',9),
	('100','CSE',10),
	('100','CSE',11),
	('100','CSE',12),
	('100','CSE',13),
	('100','CSE',14);

/*!40000 ALTER TABLE `rooms_triggers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rule_translation_dictionary
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rule_translation_dictionary`;

CREATE TABLE `rule_translation_dictionary` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `language` varchar(11) DEFAULT NULL,
  `original` varchar(255) DEFAULT NULL,
  `translation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rule_translation_dictionary` WRITE;
/*!40000 ALTER TABLE `rule_translation_dictionary` DISABLE KEYS */;

INSERT INTO `rule_translation_dictionary` (`id`, `language`, `original`, `translation`)
VALUES
	(1,'Z3','time is between @val and @val','(and (>= (time 1) @val) (<= (time 1) @val))'),
	(2,'Z3','someone is in the room','(inRoom 1)'),
	(3,'Z3','nobody is in the room','(not (inRoom 1))'),
	(4,'Z3','external temperature is between @val and @val','(and (>= (extTempInRoom 1) @val) (<= (extTempInRoom 1) @val))'),
	(5,'Z3','the date is between @val and @val','(and (>= (day 1) @val) (<= (day 1) @val))'),
	(6,'Z3','it is sunny','(sunny 1)'),
	(7,'Z3','it is rainy','(rainy 1)'),
	(8,'Z3','it is cloudy','(cloudy 1)'),
	(9,'Z3','demand reponse event','(demandeResponse 1)'),
	(10,'Z3','calendar meeting event','(meetingEvent 1)'),
	(11,'Z3','room temperature is between @val and @val','(and (>= (tempInRoom 1) @val) (<= (tempInRoom 1) @val))'),
	(12,'Z3','no rule specified','(noRule 1)'),
	(13,'Z3','today is @val','(= (today 1) @val)'),
	(14,'Z3','turn on the room light','(light 1)'),
	(15,'Z3','turn off the room light','(not (light 1))'),
	(16,'Z3','open the windows','(openWindows 1)'),
	(17,'Z3','close the windows','(not (openWindows 1))'),
	(18,'Z3','set temperature between @val and @val','(and (>= (tempSetpoint 1) @val) (<= (tempSetpoint 1) @val))'),
	(19,'Z3','set humidity between @val and @val','(and (>= (humiditySetpoint 1) @val) (<= (humiditySetpoint 1) @val))'),
	(20,'Z3','turn on the coffee machine','(coffee 1)'),
	(21,'Z3','turn off the coffee machine','(not (coffee 1))'),
	(22,'Z3','turn on the printer','(printer 1)'),
	(23,'Z3','turn off the printer','(not (printer 1))'),
	(24,'Z3','wake up my computer','(computer 1)'),
	(25,'Z3','put to sleep my computer','(not (computer 1))'),
	(26,'Z3','turn on my desk light','(deskLight 1)'),
	(27,'Z3','turn off my desk light','(not (deskLight 1))'),
	(28,'Z3','turn on display monitors','(displayMonitors 1)'),
	(29,'Z3','turn off display monitors','(not (displayMonitors 1))'),
	(30,'Z3','send complain to building manger','(sendComplain 1)'),
	(31,'Z3','open the curtains','(openCurtains 1)'),
	(32,'Z3','close the curtains','(not (openCurtains 1))'),
	(33,'Z3','turn heating, ventilation and air conditioning on','(hvac 1)'),
	(34,'Z3','turn heating, ventilation and air conditioning off','(not (hvac 1))'),
	(35,'Z3','turn on the projector','(projector 1)'),
	(36,'Z3','turn off the projector','(not (projector 1))'),
	(37,'Z3','turn on the audio system','(audio 1)'),
	(38,'Z3','turn off the audio system','(not (audio 1))'),
	(39,'Z3','turn on the exhaust fan','(exhaustFan 1)'),
	(40,'Z3','turn off the exhaust fan','(not (exhaustFan 1))'),
	(41,'Z3','turn on the fume hoods','(fumeHoods 1)'),
	(42,'Z3','turn off the fume hoods','(not (fumeHoods 1))'),
	(43,'Z3','set blind to @val','(= (blind 1) @val)'),
	(44,'Z3','the day is between @val and @val','(and (>= (today 1) @val) (<= (today 1) @val))'),
	(45,'Z3','turn on the heating','(heating 1)'),
	(46,'Z3','turn off the heating','(not (heating 1))'),
	(47,'Z3','turn on the air conditioning','(airConditioning 1)'),
	(48,'Z3','turn off the air conditioning','(not (airConditioning 1))'),
	(49,'Z3','turn on the microwave','(microwave 1)'),
	(50,'Z3','turn off the microwave','(not (microwave 1))');

/*!40000 ALTER TABLE `rule_translation_dictionary` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rules`;

CREATE TABLE `rules` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `priority` int(11) DEFAULT NULL,
  `category` varchar(24) DEFAULT NULL,
  `building_name` varchar(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `room_name` varchar(11) DEFAULT NULL,
  `author_uuid` int(11) DEFAULT NULL,
  `antecedent` varchar(255) DEFAULT NULL,
  `consequent` varchar(255) DEFAULT NULL,
  `enabled` int(1) DEFAULT NULL,
  `deleted` int(1) DEFAULT NULL,
  `creation_timestamp` timestamp NULL DEFAULT NULL,
  `last_edit_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table rules_priority
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rules_priority`;

CREATE TABLE `rules_priority` (
  `building_name` varchar(11) NOT NULL DEFAULT '0',
  `room_name` varchar(11) NOT NULL DEFAULT '0',
  `rule_id` int(11) NOT NULL DEFAULT '0',
  `rule_priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`building_name`,`room_name`,`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table sessions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sessions`;

CREATE TABLE `sessions` (
  `session_key` varchar(64) NOT NULL DEFAULT '',
  `user_uuid` int(11) DEFAULT NULL,
  `expire_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table triggers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `triggers`;

CREATE TABLE `triggers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(16) DEFAULT NULL,
  `trigger_name` varchar(24) DEFAULT NULL,
  `rule_antecedent` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `triggers` WRITE;
/*!40000 ALTER TABLE `triggers` DISABLE KEYS */;

INSERT INTO `triggers` (`id`, `category`, `trigger_name`, `rule_antecedent`, `description`)
VALUES
	(1,'OCCUPANCY','OCCUPANCY_TRUE','someone is in the room','check if someone is in the room'),
	(2,'OCCUPANCY','OCCUPANCY_FALSE','nobody is in the room','check if nobody is in the room'),
	(3,'EXT_TEMPERATURE','EXT_TEMPERATURE_RANGE','external temperature is between @val and @val','check temperature'),
	(4,'TIME','TIME_RANGE','time is between @val and @val','check time'),
	(5,'DATE','DATE_RANGE','the date is between @val and @val','check day'),
	(6,'WEATHER','SUNNY','it is sunny','check the weather'),
	(7,'WEATHER','RAINY','it is rainy','check the weather'),
	(8,'ROOM_TEMPERATURE','ROOM_TEMPERATURE_RANGE','room temperature is between @val and @val','check temperature'),
	(9,'WEATHER','CLOUDY','it is cloudy','check the weather'),
	(10,'DEFAULT_STATUS','NO_RULE','no rule specified','default rule'),
	(11,'DAY','TODAY','today is @val','rules for the current day'),
	(12,'EXTERNAL_APP','DEMANDE_REPONSE','demand response event','demand response event'),
	(13,'EXTERNAL_APP','CALENDAR_MEETING','calendar meeting event','calendar meeting event'),
	(14,'DAY','DAY_RANGE','the day is between @val and @val','check day');

/*!40000 ALTER TABLE `triggers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `uuid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(11) NOT NULL DEFAULT '',
  `email` varchar(64) DEFAULT NULL,
  `password` varchar(128) NOT NULL DEFAULT '',
  `person_name` varchar(24) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `registration_timestamp` timestamp NULL DEFAULT '2014-01-01 08:00:00',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`uuid`, `username`, `email`, `password`, `person_name`, `level`, `registration_timestamp`)
VALUES
	(1,'user','user','user','user',10,'2014-01-01 08:00:00');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users_rooms
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_rooms`;

CREATE TABLE `users_rooms` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `user_uuid` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`user_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users_rooms` WRITE;
/*!40000 ALTER TABLE `users_rooms` DISABLE KEYS */;

INSERT INTO `users_rooms` (`room_name`, `building_name`, `user_uuid`)
VALUES
	('100','CSE',1);

/*!40000 ALTER TABLE `users_rooms` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
