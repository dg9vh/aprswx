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

### Configuration of the weather-stations in `staions.py`
The weather-stations are configured by filling the infos into the 
configuration-array as given in the example. Here is the meaning of: * 
station-ID: Callsign of the station in aprs.fi * QTH: Location of the 
station * DAPNET-rubric: Rubric on DAPNET, to which the weather-message 
should be posted * message-slot: Number of the message-slot (between 1 
to 10), on that the message should be placed `#!/usr/bin/python` `# -*- 
coding: utf-8 -*-` 

`stations = [` 

`# Formatdescription:` 

`# station-ID, QTH, DAPNET-rubric, message-slot` 

` ["CW3322","Geislautern","wetter-sl",1],` 

` ["DC0VZ-6","Gersweiler","wetter-sl",2],` 

` ["DF5VL-5","Puettlingen","wetter-sl",3],` 

` ["EW9191","Neunkirchen","wetter-sl",4],` 

` ["CW8033","Illingen","wetter-sl",5],` `]`

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
## Usage
This software is for usage on amateur radio only! 73 de Kim DG9VH
