# aprswx - sending weather messages from aprs.fi to DAPNET
## What this is doing
The script `aprswx.py` fetches wather information from aprs.fi on listed 
stations in `stations.py` and sends these into predefined rubrics in 
DAPNET to be published via POCSAG.
## Configuration
Basic configuration is done in two files:
### Configuration of your credentials in `credentials.py`
Fill the corresponding variables with your information: 
`#!/usr/bin/python` 
`# -*- coding: utf-8 -*-` 
`dapnetuser="YOURDAPNETWEB-USERNAME"` 
`dapnetpasswd="YOURDAPNETWEB-PASSWORD"` 
`aprsapikey="YOURAPRS.FI-APIKEY"`

### Configuration of the weather-stations in `stations.py`
The weather-stations are configured by filling the infos into the 
configuration-array as given in the example. Here is the meaning of: 
* callsign: Callsign of the station in aprs.fi 
* qth: Location of the station 
* rubric: Rubric on DAPNET, to which the weather-message should be posted 
* slot: Number of the message-slot (between 1 to 10), on that the message should be placed 

### Configuration of the rubrics in `rubrics.py`
This file controls from which region the WX data are fetched. Please
note that you need authorized for sending data to the rubric.

## Installation in crontab
To run the script periodically, it would be recommended to place it 
within your users crontab with `crontab -e`. Here you could use 
following line: 

` */20 * * * * cd /path/to/aprswx.py && ./aprswx.py > /dev/null` 

This would send out the weather-messages 3 time an hour on 0, 
20 and 40 minutes.
## Credits
Credits goes to the DAPNET-team (see https://hampager.de), which 
provides a wonderful POCSAG-Network on amateur radio.

Also credits are going to aprs.fi for providing the wx-data via it's API.

## Usage
This software is for usage on amateur radio only! 73 de Kim DG9VH
