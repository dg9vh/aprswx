#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
import time
from requests.auth import HTTPBasicAuth

execfile("credentials.py")
execfile("stations.py")
execfile("rubrics.py")

# Split array into smaller portions
def chunks(l,n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

# check response from DAPNET
def check_response(resp):
	if resp.status_code != 201:
		error = json.loads(resp.text)
                print error
		print "Error at", station[0]
		print('POST /news/ {}'.format(resp.status_code))

# Send data from wx station to dapnet
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
        check_response(resp)

	# this is a work-around for mirroring messages into another rubric 
	if station["rubric"] == "aprswx-dl-bw":
		post={ "rubricName": "hochrhein", "text": msg, "number": station["slot"] }
		print post
		resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
		check_response(resp)

# let the party begin!
selected_stations=""
querystring=""

# the following has to be done for each WX-station in the list
for i in range(0,len(stations)):

        # Build a string with all stations selected by rubrics
        if [ stations for rubric in rubrics if stations[i]['rubric'] == rubric['rubric'] ]:
          selected_stations+=stations[i]["callsign"]+","

# due to query-rate-limits on aprs.fi and maximum of 20 stations per
# query we have to work in portions
for line in list(chunks(selected_stations.split(","),20)):
	querystring = ",".join(line)
	# fetching data from aprs.fi
	response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
	wx = json.loads(response.text)
	entries = (wx["entries"])

	# lets do something good with the stuff we got
	for entry in entries:
		station = (item for item in stations if item["callsign"] == entry["name"]).next()
		# calling send-function above
		send_DAPNET(entry, station)
