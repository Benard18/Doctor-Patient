"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
			if flags else tools.run(flow,store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


# Call the Calendar API
# attendees=[{'email':x} for x in emails]
GMT_OFF = '+03:00'
EVENT = {
	'summary': 'Appointments',
	'start': {'dateTime':'2018-07-25T10:00:00%s' % GMT_OFF},
	'end':   {'dateTime':'2018-07-25T12:00:00%s' % GMT_OFF},
	'attendees':[
		{'email':'xavierkibet@gmail.com'},
	],
}

e = service.events().insert(calendarId='primary',
	sendNotifications=True, body=EVENT).execute()

print('''*** %r event added
	Start: %s
	End: %s'''% (e['summary'].encode('utf-8'),
	e['start']['dateTime'],e['end']['dateTime']))
