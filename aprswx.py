#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
import time
import sys
from requests.auth import HTTPBasicAuth

reload(sys)
sys.setdefaultencoding('utf8')

execfile("credentials.py")
execfile("stations.py")

debug = False
try:
	if sys.argv[1] == "-d" or sys.argv[1] == "--d":
		debug = True
except:
	pass

target_area = ""

try:
        if sys.argv[2] == "-t" or sys.argv[1] == "--target":
                target_area = "aprswx-"+sys.argv[3]
except:
        pass

print target_area

def send_DAPNET(entry, station):
	# This function is for creating and sending messages to DAPNET
	# attention: Timestamp in aprs.fi is epoch!
	ts_epoch = float(entry["time"])
	# so lets calculate and format in hhmm-format
	msgtime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%H%M')
	msgtime_raw = datetime.datetime.fromtimestamp(ts_epoch)
	nowtime = datetime.datetime.now()
	difference = nowtime - msgtime_raw
	difference_days = difference.days
	if difference_days > 0:
		print "Message outdated for ", station["callsign"]
		return
	# now it's time for building up the message itself
	msg = msgtime + "z " + station["callsign"] + "/" + station["qth"] + ": "
	highwinds = False
	# WX-data in try-blocks, because not every WX-station delivers all data
	try:
		print station["unit"]
		if station["unit"] == "c":
			temperature = entry["temp"] + "C "
			msg+=temperature
		if station["unit"] == "f":
			temperature = float(entry["temp"])
			fahrenheit = 9.0/5.0 * temperature + 32.0
			temperature = str(round(fahrenheit,1)) + "F "
			msg+=temperature
	except:
		pass

	try:
		if float(entry["wind_speed"]) == 0:
			wind = "w: no "
		else:
			wind = "w: " + entry["wind_speed"]+ "m/s=" + entry["wind_direction"] + "deg "
		msg+=wind
		if float(entry["wind_speed"]) > 10:
			highwinds = True
			msg += "high! "
	except:
		pass

	try:
		humidity = "h: " + entry["humidity"] + "% "
		msg+=humidity
	except:
		pass

	try:
		pressure = "hPa: " + entry["pressure"] + " "
		msg+=pressure
	except:
		pass

	try:
		rain = "r: " + entry["rain_1h"] + "mm/h"
		msg+=rain
	except:
		pass

	# preparing the post-message
	post={ "rubricName": station["rubric"], "text": msg[:80], "number": station["slot"] }
	print post , len(msg)
	if len(msg) > 80:
		print "Message too long!!!", station["callsign"]
	sendingtime = datetime.datetime.now().hour%4
	if debug:
		print "Debug mode ON"
		sendingtime = 0
	else:
		print "Debug mode OFF"
	if highwinds or 0 == sendingtime:
		# and sending it to DAPNET
		print "Sending to DAPNET"

#		resp = requests.post('https://hampager.de/api/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
		resp = requests.post('http://44.149.166.27:8080/news/', json=post, auth=HTTPBasicAuth(dapnetuser, dapnetpasswd))
		if resp.status_code != 201:
			print "Error at", station["callsign"]
			print('POST /news/ {}'.format(resp.status_code))
		else:
			print "Message sent for ", station["callsign"]
		time.sleep(2)


# let the party begin!
stations_count = len(stations)
querystring=""

# the following has to be done for each WX-station in the list
for i in range(0,stations_count):
	# due to query-rate-limits on aprs.fi and maximum of 20 stations per
	# query we have to work in portions
	if i > 0 and (i % 20) == 0:
		# fetching data from aprs.fi
		querystring=querystring[:-1]
		print "Query APRS.fi: " + querystring
		response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
		wx = json.loads(response.text)
		entries = (wx["entries"])

		# lets do something good with the stuff we got
		for entry in entries:
			try:
				station = (item for item in stations if item["callsign"] == entry["name"]).next()
				# calling send-function above
				if target_area != "":
					if target_area == station["rubric"]:
						send_DAPNET(entry, station)
				else:
					send_DAPNET(entry, station)
#				time.sleep(5)
			except:
				print "No data from %s \n" %(entry["name"])
				pass
		querystring = "";
	querystring+=stations[i]["callsign"]+","

querystring=querystring[:-1]
# now we have a few stations left to procede, so lets do the rest here,
# same as above, as you see
response = requests.get("https://api.aprs.fi/api/get?name="+querystring+"&what=wx&apikey="+aprsapikey+"&format=json")
wx = json.loads(response.text)
entries = (wx["entries"])
for entry in entries:
	try:
		station = (item for item in stations if item["callsign"] == entry["name"]).next()
#		send_DAPNET(entry, station)
		if target_area != "":
			if target_area == station["rubric"]:
				send_DAPNET(entry, station)
		else:
			send_DAPNET(entry, station)

	except:
		print "No data from %s \n" %(entry["name"])
		pass
