import sys
import datetime
import time
import signal
import os.path
import json
import httplib2
import urllib
import os
from dateutil.tz import tzlocal

#ob-ucsd-cse.ucsd.edu:8000/dataservice/
#sensor_type = 'Zone Temperature'
#zone = 'RM-B200B'
#BD api key: 7d0a9b2f-11bd-40da-8ff5-f7836fe468c3
#auth_token: 1


def get_uuid_from_context(sensor_type, zone):
    try:
        response = http.request(
        "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/context/Type=" + sensor_type + "+Room=Rm-" + zone,
        "GET",
        headers={'content-type':'application/json', 'X-BD-Api-Key': api_key, 'X-BD-Auth-Token': auth_token}
        )
        #print "response: ", response

    except Exception as e:
        print "Could not search by given context"
        print "Error: ", e
        return None 

    response = response[1]
    response_json = json.loads(response) 
    sensors_list = response_json["sensors"]

    try:
        uuid = sensors_list[0]["uuid"]
    except Exception as e: 
        print "Could not extract uuid out of response"
        print "Error: ", e
        return None 
    
    #print "Sensor uuid is " + uuid
    
    return uuid

def read_present_value_by_uuid(sensor_uuid, sensorpoint_name = "PresentValue"):
    url = "http://ob-ucsd-cse.ucsd.edu:8000/dataservice/api/sensors/" + sensor_uuid + "/sensorpoints/" + sensorpoint_name + "/datapoints"

    try:
        response = http.request(
        url,
        "GET",
        headers={"X-BD-Api-Key": api_key, "X-BD-Auth-Token": auth_token}
        )
        #print response
        response_json = json.loads(response[1])
        datapoints = response_json["datapoints"]
        for time, data in datapoints[0].iteritems():
            value = float(data)
    except Exception as e:
        print "Error, could not read present value: ", e
        return None

    return value