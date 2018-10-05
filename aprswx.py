#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
import time
from requests.auth import HTTPBasicAuth

execfile("credentials.py")
execfile("stations.py")

def send_DAPNET(entry, station):
	ts_epoch = float(entry["time"])
	msgtime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H%M')
	msg = msgtime + "z " + station["callsign"] + "/" + station["qth"] + ": "
	try:
		temperature = entry["temp"] + "C "
		msg+=temperature
	except:
		pass

	try:
		wind = "w: " + entry["wind_speed"]+ "m/s at " + entry["wind_direction"] + "deg "
		msg+=wind
	except:
		pass

	try:
		humidity = "h: " + entry["humidity"] + "% "
		msg+=humidity
	except:
		pass

	try:
		rain = "rain: " + entry["rain_1h"] + "mm/h"
		msg+=rain
	except:
		pass

	post={ "rubricName": station["rubric"], "text": msg, "number": station["slot"] }
	print post
	resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
	if resp.status_code != 201:
		print "Error at", station[0]
		print('POST /news/ {}'.format(resp.status_code))
	if station["rubric"] == "aprswx-dl-bw":
		post={ "rubricName": "hochrhein", "text": msg, "number": station["slot"] }
		print post
		resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
		if resp.status_code != 201:
			print "Error at", station[0]
			print('POST /news/ {}'.format(resp.status_code))


stations_count = len(stations)
print stations_count
querystring=""
for i in range(0,stations_count):
	if i > 0 and (i % 20) == 0:
		print querystring
		response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
		wx = json.loads(response.text)
		entries = (wx["entries"])
		for entry in entries:
			station = (item for item in stations if item["callsign"] == entry["name"]).next()
			send_DAPNET(entry, station)
#			time.sleep(8)

		querystring = "";
	querystring+=stations[i]["callsign"]+","

print querystring
response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
wx = json.loads(response.text)
entries = (wx["entries"])
for entry in entries:
	station = (item for item in stations if item["callsign"] == entry["name"]).next()
	send_DAPNET(entry, station)
'''
response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
wx = json.loads(response.text)
print wx

	entries = (wx["entries"])
	ts_epoch = float(entries[0]["time"])
	msgtime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H%M')
	msg = msgtime + "z " + station[0] + "/" + station[1] + ": "
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
	time.sleep(8)
'''
