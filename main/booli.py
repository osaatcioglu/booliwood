import httplib
import time
from hashlib import sha1
import random
import string
import json
import urllib

def booliwood(query, offset, limit, type):
	# get your api key from http://www.booli.se/api/key
	callerId = "< Caller ID >"
	privateKey = "< YOUR PRIVATE KEY >"
	timestamp = str(int(time.time()))
	unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
	hashstr = sha1(callerId+ timestamp + privateKey + unique).hexdigest()
	 
	search_query = {
	"q" : query,
	"callerId" : callerId,
	"time" : timestamp,
	"unique" :unique,
	"hash" :hashstr,
	"offset" : str(offset),
	"limit" : str(limit)
	}

	url = "/" + type + "?" + urllib.urlencode(search_query)

	connection = httplib.HTTPConnection("api.booli.se")
	connection.request("GET", url)
	response = connection.getresponse()
	data = response.read()
	connection.close()
	 
	if response.status != 200:
	    print "fail"
	 
	result = json.loads(data)
	return result