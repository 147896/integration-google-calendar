
Python script to integrate google calendar. Obtains the token from the SSO system and submits a request to the intranet portal and extracts the point information, handles with an HTML parser and registers in Google Calendar.

Python script to integrate google calendar. Obtains the token from the SSO
system and submits a request to the intranet portal and extracts the point
information, handles with an HTML parser and registers in Google Calendar.

Libraries used: 

Python script to OpenAM SSO authenticate and request Portal.
- auth_portal.py:  
import requests, json, sys, os, re, smtplib, time  
from datetime import datetime, timedelta, time  
from requests.packages.urllib3.exceptions import InsecureRequestWarning

Python script to create events.
- gr_event_ponto.py:  
See google documentation API - https://developers.google.com/calendar/create-events

Python script to get string date, convert to date format and calculate specific
registers.
- testedate.py:  
from datetime import datetime, timedelta, time  
import sys  
from auth_portal import entrada, almoco_in, almoco_out, oam_logout
