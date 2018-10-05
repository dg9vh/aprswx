#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
import time
from requests.auth import HTTPBasicAuth

execfile("credentials.py")
execfile("stations.py")

for station in stations:
	response = requests.get("https://api.aprs.fi/api/get?name="+station[0]+"&what=wx&apikey="+aprsapikey+"&format=json")
	wx = json.loads(response.text)
	entries = (wx["entries"])
	ts_epoch = float(entries[0]["time"])
	msgtime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H:%M')
	msg = msgtime + " " + station[0] + "/" + station[1] + ": "
	try:
		temperature = entries[0]["temp"] + "C "
		msg+=temperature
	except:
		pass

	try:
		wind = "w: " + entries[0]["wind_speed"]+ "m/s at " + entries[0]["wind_direction"] + "deg "
		msg+=wind
	except:
		pass

	try:
		humidity = "h: " + entries[0]["humidity"] + "% "
		msg+=humidity
	except:
		pass

	try:
		rain = "rain: " + entries[0]["rain_1h"] + "mm/h"
		msg+=rain
	except:
		pass

	post={ "rubricName": station[2], "text": msg, "number": station[3] }
	print post
	resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
	if resp.status_code != 201:
		print "Error at", station[0]
		print('POST /news/ {}'.format(resp.status_code))
	time.sleep(5)
