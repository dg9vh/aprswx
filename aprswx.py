#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
from requests.auth import HTTPBasicAuth

execfile("credentials.py")
execfile("stations.py")

for station in stations:
	response = requests.get("https://api.aprs.fi/api/get?name="+station[0]+"&what=wx&apikey="+aprsapikey+"&format=json")
	wx = json.loads(response.text)
	entries = (wx["entries"])
	ts_epoch = float(entries[0]["time"])
	time = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H:%M')
	msg = time + " " + station[0] + "/" + station[1] + ": " + entries[0]["temp"] + "C w: " + entries[0]["wind_speed"] + "m/s at " + entries[0]["wind_direction"] + "deg h: " + entries[0]["humidity"] + "% rain: " + entries[0]["rain_1h"] + "mm/h"
	post={ "rubricName": station[2], "text": msg, "number": station[3] }
	resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
	if resp.status_code != 201:
		print "Error at", station[0]
		print('POST /news/ {}'.format(resp.status_code))
