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
	# This function is for creating and sending messages to DAPNET

	# attention: Timestamp in aprs.fi is epoch!
	ts_epoch = float(entry["time"])
	# so lets calculate and format in hhmm-format
	msgtime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H%M')

	# now it's time for building up the message itself
	msg = msgtime + "z " + station["callsign"] + "/" + station["qth"] + ": "

	# WX-data in try-blocks, because not every WX-station delivers all data
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

	# preparing the post-message
	post={ "rubricName": station["rubric"], "text": msg, "number": station["slot"] }
	print post

	# and sending it to DAPNET
	resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
	if resp.status_code != 201:
		print "Error at", station[0]
		print('POST /news/ {}'.format(resp.status_code))

	# this is a work-around for mirroring messages into another rubric 
	if station["rubric"] == "aprswx-dl-bw":
		post={ "rubricName": "hochrhein", "text": msg, "number": station["slot"] }
		print post
		resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
		if resp.status_code != 201:
			print "Error at", station[0]
			print('POST /news/ {}'.format(resp.status_code))


# let the party begin!
stations_count = len(stations)
querystring=""

# the following has to be done for each WX-station in the list
for i in range(0,stations_count):
	# due to query-rate-limits on aprs.fi and maximum of 20 stations per
	# query we have to work in portions
	if i > 0 and (i % 20) == 0:
		# fetching data from aprs.fi
		response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
		wx = json.loads(response.text)
		entries = (wx["entries"])

		# lets do something good with the stuff we got
		for entry in entries:
			station = (item for item in stations if item["callsign"] == entry["name"]).next()
			# calling send-function above
			send_DAPNET(entry, station)
		querystring = "";
	querystring+=stations[i]["callsign"]+","

# now we have a few stations left to procede, so lets do the rest here,
# same as above, as you see
response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
wx = json.loads(response.text)
entries = (wx["entries"])
for entry in entries:
	station = (item for item in stations if item["callsign"] == entry["name"]).next()
	send_DAPNET(entry, station)
