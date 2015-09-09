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

from app import app
import requests
import json

def request(url, data = {}):


	keyToRemove = []
	for key, value in data.iteritems():
		keyToken = "<" + key + ">"
		if keyToken in url:
			url = url.replace(keyToken, str(value))
			keyToRemove.append(key)



	for key in keyToRemove:
		del data[key]

	#url = "http://" + app.config['API_SERVER_IP'] + ":" + str(app.config['API_SERVER_PORT']) + url
	headers = {'Accept-Language': 'en-us', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate'}
	
	print "API_REQUEST: Contacting " + url + " with params " + str(data)

	r = requests.post(url, data=data, headers=headers)

	if r.status_code == 200:
		response = json.loads(r.text)

		if 'request-success' not in response.keys() and 'request-error' not in response.keys():
			response = {}
			response["request-success"] = False
			response["request-error"] = True
			response["request-errorName"] = "InvalidAPIReply"
			response["request-errorDescription"] = "The API reply is not well-formed."

	else:
		response = {}
		response["request-success"] = False
		response["request-error"] = True
		response["request-errorName"] = "APIRequestFailed"
		response["request-errorDescription"] = str(r.status_code) + " - " + getHTTPErrorDescription(r.status_code)

	return response

def getHTTPErrorDescription(error_code):
	HTTP_ERROR = {}
	
	HTTP_ERROR[100] = "Continue: The server has received the request headers, and the client should proceed to send the request body"
	HTTP_ERROR[101] = "Switching Protocols: The requester has asked the server to switch protocols"
	HTTP_ERROR[103] = "Checkpoint: Used in the resumable requests proposal to resume aborted PUT or POST requests"
	HTTP_ERROR[200] = "OK: The request is OK (this is the standard response for successful HTTP requests)"
	HTTP_ERROR[201] = "Created: The request has been fulfilled, and a new resource is created "
	HTTP_ERROR[202] = "Accepted: The request has been accepted for processing, but the processing has not been completed"
	HTTP_ERROR[203] = "Non-Authoritative Information: The request has been successfully processed, but is returning information that may be from another source"
	HTTP_ERROR[204] = "No Content: The request has been successfully processed, but is not returning any content"
	HTTP_ERROR[205] = "Reset Content: The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view"
	HTTP_ERROR[206] = "Partial Content: The server is delivering only part of the resource due to a range header sent by the client"
	HTTP_ERROR[300] = "Multiple Choices: A link list. The user can select a link and go to that location. Maximum five addresses  "
	HTTP_ERROR[301] = "Moved Permanently: The requested page has moved to a new URL "
	HTTP_ERROR[302] = "Found: The requested page has moved temporarily to a new URL "
	HTTP_ERROR[303] = "See Other: The requested page can be found under a different URL"
	HTTP_ERROR[304] = "Not Modified: Indicates the requested page has not been modified since last requested"
	HTTP_ERROR[306] = "Switch Proxy: No longer used"
	HTTP_ERROR[307] = "Temporary Redirect: The requested page has moved temporarily to a new URL"
	HTTP_ERROR[308] = "Resume Incomplete: Used in the resumable requests proposal to resume aborted PUT or POST requests"
	HTTP_ERROR[400] = "Bad Request: The request cannot be fulfilled due to bad syntax"
	HTTP_ERROR[401] = "Unauthorized: The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided"
	HTTP_ERROR[402] = "Payment Required: Reserved for future use"
	HTTP_ERROR[403] = "Forbidden: The request was a legal request, but the server is refusing to respond to it"
	HTTP_ERROR[404] = "Not Found: The requested page could not be found but may be available again in the future"
	HTTP_ERROR[405] = "Method Not Allowed: A request was made of a page using a request method not supported by that page"
	HTTP_ERROR[406] = "Not Acceptable: The server can only generate a response that is not accepted by the client"
	HTTP_ERROR[407] = "Proxy Authentication Required: The client must first authenticate itself with the proxy"
	HTTP_ERROR[408] = "Request Timeout: The server timed out waiting for the request"
	HTTP_ERROR[409] = "Conflict: The request could not be completed because of a conflict in the request"
	HTTP_ERROR[410] = "Gone: The requested page is no longer available"
	HTTP_ERROR[411] = "Length Required: The 'Content-Length' is not defined. The server will not accept the request without it "
	HTTP_ERROR[412] = "Precondition Failed: The precondition given in the request evaluated to false by the server"
	HTTP_ERROR[413] = "Request Entity Too Large: The server will not accept the request, because the request entity is too large"
	HTTP_ERROR[414] = "Request-URI Too Long: The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information "
	HTTP_ERROR[415] = "Unsupported Media Type: The server will not accept the request, because the media type is not supported "
	HTTP_ERROR[416] = "Requested Range Not Satisfiable: The client has asked for a portion of the file, but the server cannot supply that portion"
	HTTP_ERROR[417] = "Expectation Failed: The server cannot meet the requirements of the Expect request-header field"
	HTTP_ERROR[500] = "Internal Server Error: A generic error message, given when no more specific message is suitable"
	HTTP_ERROR[501] = "Not Implemented: The server either does not recognize the request method, or it lacks the ability to fulfill the request"
	HTTP_ERROR[502] = "Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server"
	HTTP_ERROR[503] = "Service Unavailable: The server is currently unavailable (overloaded or down)"
	HTTP_ERROR[504] = "Gateway Timeout: The server was acting as a gateway or proxy and did not receive a timely response from the upstream server"
	HTTP_ERROR[505] = "HTTP Version Not Supported: The server does not support the HTTP protocol version used in the request"
	HTTP_ERROR[511] = "Network Authentication Required: The client needs to authenticate to gain network access"

	return HTTP_ERROR[int(error_code)]