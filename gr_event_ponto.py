#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime, time
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from auth_portal import *
from testedate import saida_prevista

# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('/root/scripts/token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/root/scripts/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
eventss = {
  'summary': '%s - Retorno almoço.' %(retorno_almoco),
  'location': 'Unimed-BH, inconfidentes, 44',
  'description': 'Marcações do ponto Unimed-BH.\n\
   resumo das marcações:\n\
   Entrada.: %s\n\
   Saida Almoço.: %s\n\
   Retorno Almoço.: %s\n\
   Saida.: %s\n\
   Saida geral prevista.: %s\n' %(entrada, almoco_in, almoco_out, saida, saida_prevista),
  'start': {
    'dateTime': '%sT%s:00' %(complete_today, almoco_in),
    'timeZone': 'America/Sao_Paulo',
  },
  'end': {
    'dateTime': '%sT%s' %(complete_today, retorno_almoco),
    'timeZone': 'America/Sao_Paulo',
  },
  'attendees': [
    {'email': 'gabriel.ribass@gmail.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'popup', 'minutes': 1},
    ],
  },
}

#if not almoco_in == '--':
print(eventss)
event = service.events().insert(calendarId='primary', body=eventss).execute()
print('Google calendar event created')
#else:
#   print('Nenhum registro encontrado..')
