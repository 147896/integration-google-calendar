#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Lets try to hack the intranet.
# Create by Python Developer Gabriel Ribas (gabriel.ribass@gmail.com),
# in 2018-10-18 - Brazil.
# This script would be to authenticate in OpenAM server and access
# the portal intranet Unimed-BH.
# The end of this story only God can unveil °/°
#					    (-)
import requests, json, sys, os, re, smtplib
from datetime import datetime, timedelta
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#log file create
logfile = open('/tmp/intranet.log', 'a')

#init connection smtp
server = smtplib.SMTP('uniweb135.unimedbh.com.br', 25)

#verify portal intranet date registred in file
date_file_read = open('/tmp/ponto.txt', 'r')
date_string = date_file_read.read().strip('\n')

#verify system date
date = datetime.now()
today = date.strftime('%d')

dayago_ = date - timedelta(days=1)
dayago = dayago_.strftime('%d')

if not '%s' %(today) in date_string:
   date_file_write = open('/tmp/ponto.txt', 'w')

# Portal intranet date validate. If already registred. 
# This prevent new requests against portal intranet
if date_string == today:
   print("Already registred..")
   logfile.write('%s, Point already registred..\n' %(date))
   logfile.close()
   sys.exit(0)

# OpenAM credentials - Token
print("Autenticando no OpenAM")
username = "uni13477"
password = "T3hil1m128"
oam = "https://extranet.unimedbh.com.br/openam/json/"
app = "https://portal.unimedbh.com.br/wps/myportal/novaintranet/home"

# OpenAM endpoints
authenticate = oam + "authenticate"
sessions = oam + "sessions"
users = oam + "users"

# OpenAM Authenticate
payload = "{\"uri\": \"ldapService\"}"
headers = {
      'X-OpenAM-Username': "uni13477",
      'X-OpenAM-Password': "T3hil1m128",
      'Content-Type': "application/json"
      }
try:
   response = requests.post(authenticate, data=payload, headers=headers)
   tokenid = json.loads(response.text)
   cookie = response.cookies
   cookie.set('LtpaToken', '%s' %(cookie['LtpaToken']), domain='.unimedbh.com.br', path='/')
   cookie.set('LtpaToken2', '%s' %(cookie['LtpaToken2']), domain='.unimedbh.com.br', path='/')
   cookie.set('amlbcookie', '%s' %(cookie['amlbcookie']), domain='.unimedbh.com.br', path='/')
   cookie.set('TMP_COOKIE_AX_EXTRANET', '%s' %(cookie['TMP_COOKIE_AX_EXTRANET']), domain='extranet.unimedbh.com.br', path='/')
   cookie.set('iPlanetDirectoryPro', '%s' %(tokenid['tokenId']), domain='.unimedbh.com.br', path='/')
except:
   print(response.text)
   logfile.write('%s, ERROR.: %s\n' %(date, response.text))
   logfile.close()
   sys.exit(2)


# GET Portal Intranet - tag registro de ponto
print("Acessando o Portal Intranet")
response = requests.get(app, cookies=cookie)
result = response.text.encode('utf-8')


#find date portal
find_date = re.search('(.*\s<p>[0-9]\w+<span>[a-z]\w+<\/span><\/p>)', result)
field_date = find_date.group(0).split('<span>')
pod = list(field_date)
data_hoje = re.sub(r'(.*\s<p>)', '', pod[0])

#find hour portal
find_hour = re.search('(<li class="entrada" title=".*[a-zA-Z]*."><p>*.*<\/p><\/li><li class="almoco_in" title=".*[a-zA-Z]*."><p>*.*<\/p><\/li><li class="almoco_out" title=".*[a-zA-Z]*."><p>*.*<\/p><\/li><li class="saida" title=".*[a-zA-Z]*."><p>*.*<\/p><\/li>)', result)
field_hour = find_hour.group(0).split('<p>')
poh = list(field_hour)
entrada = re.sub(r'(<\/p>.*)', '', poh[1])
almoco_in = re.sub(r'(<\/p>.*)', '', poh[2])
almoco_out = re.sub(r'(<\/p>.*)', '', poh[3])
saida = re.sub(r'(<\/p>.*)', '', poh[4])


# SMTP message format and sendmail
msg = MIMEMultipart()
msg['From'] = 'gabriel.ribas@unimedbh.com.br'
msg['To'] = 'gabriel.ribass@gmail.com'
msg['Subject'] = 'Registro de ponto Unimed-BH'
body = "Registro de ponto Unimed-BH - Gabriel Ribas\n\
	---\n\
	Entrada.: %s\n\
	Saida Almoco.: %s\n\
	Retorno Almoco.: %s\n\
	Saida.: %s\
       " %(entrada, almoco_in, almoco_out, saida)
msg.attach(MIMEText(body, 'plain'))
text = msg.as_string()

if entrada == '--' and almoco_in == '--' and almoco_out == '--' and saida == '--':
   print('point is not resgistred yet..')
   logfile.write('%s, no marking identified..\n' %(date))
   logfile.close()
   sys.exit(0)
if not almoco_in == '--':
   #server.sendmail("gabriel.ribas@unimedbh.com.br", "gabriel.ribass@gmail.com", text)
   #call google calendar event..
   #event
   print("Unimed-BH point info sent to Gabriel Ribas")
   logfile.write('%s, Unimed-BH point info sent to Gabriel Ribas\n' %(date))
   logfile.close()
   # insert portal intranet date
   date_file_write.write('%s\n' %(today)) # isso aqui est'a l'a no topo..
   date_file_write.close()
else:
   print("no lunch registred yet..")
   logfile.write('%s, no lunch marking identifies yet..\n' %(date))
   logfile.close()
   sys.exit(0)

# OpenAM logout
querystring = {"_action":"logout"}
headers = {
      'iPlanetDirectoryPro': "%s" %(tokenid['tokenId']),
      'Content-Type': "application/json"
      }
try:
   print("OpenAM Logout..")
   requests.post(sessions, headers=headers, params=querystring)
except:
   print("houve algum erro ao tentar fazer logout no OAM..")
   logfile.write('%s ERROR.: OpenAM Logout error..\n' %(date))
   logfile.close()

#close ponto.txt file..
date_file_read.close()

#close connection smtp
server.quit()

#logs
logfile.close()
