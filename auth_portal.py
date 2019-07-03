#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Lets try to hack the intranet.
# Create by Python Developer Gabriel Ribas (gabriel.ribass@gmail.com),
# in 2018-10-18 - Brazil.
# This script would be to authenticate in OpenAM server and access
# the portal intranet Unimed-BH.
# The end of this story only God can unveil °/°
#					    (-)
import requests, json, sys, os, re, smtplib, time
from datetime import datetime, timedelta, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logfile = open('/tmp/intranet.log', 'a')

#verify portal intranet date registred in file
date_file_read = open('/tmp/ponto.txt', 'r')
date_string = date_file_read.read().strip('\n')

#verify system date
date = datetime.now()
today = date.strftime('%d')
complete_today = date.strftime('%Y-%m-%d')

dayago_ = date - timedelta(days=1)
dayago = dayago_.strftime('%d')

#if not '%s' %(today) in date_string:
if not '%s_almoco_in' %(today) in date_string or not '%s_almoco_out' %(today) in date_string:
   date_file_write = open('/tmp/ponto.txt', 'a')

# Portal intranet date validate. If already registred. 
# This prevent new requests against portal intranet
if '%s_almoco_in' %(today) in date_string and '%s_almoco_out' %(today) in date_string:
   print("Already registred..")
   logfile.write('%s, Point already registred..\n' %(date))
   logfile.close()
   sys.exit(0)

# OpenAM credentials - Token
print("Autenticando no OpenAM")
username = "uni13477"
password = "P@ssw0rd"
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
      'X-OpenAM-Password': "P@ssw0rd",
      'Content-Type': "application/json"
      }
try:
   response = requests.post(authenticate, data=payload, headers=headers, verify=False)
   tokenid = json.loads(response.text)
   cookie = response.cookies
   cookie.set('LtpaToken', '%s' %(cookie['LtpaToken']), domain='.unimedbh.com.br', path='/')
   cookie.set('LtpaToken2', '%s' %(cookie['LtpaToken2']), domain='.unimedbh.com.br', path='/')
   cookie.set('amlbcookie', '%s' %(cookie['amlbcookie']), domain='.unimedbh.com.br', path='/')
   cookie.set('TMP_COOKIE_AX_EXTRANET', '%s' %(cookie['TMP_COOKIE_AX_EXTRANET']), domain='extranet.unimedbh.com.br', path='/')
   cookie.set('iPlanetDirectoryPro', '%s' %(tokenid['tokenId']), domain='.unimedbh.com.br', path='/')
except:
   print(response.text)
   print(authenticate)
   logfile.write('%s, ERROR.: %s\n' %(date, response.text))
   logfile.close()
   sys.exit(2)


# GET Portal Intranet - tag registro de ponto
print("Acessando o Portal Intranet")
response = requests.get(app, cookies=cookie, verify=False)
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

if entrada == '--' and almoco_in == '--' and almoco_out == '--' and saida == '--':
   print('point is not resgistred yet..')
   logfile.write('%s, no marking identified..\n' %(date))
   logfile.close()

# para saber que a entrada almoco foi marcada..
if '%s_almoco_in' %(today) in date_string:
   pass
#elif not almoco_in == '--' or not '%s_almoco_in' %(today) in date_string:
#   almoco_in_format = datetime.strptime(almoco_in, '%H:%M').time()
#   retorno_almoco = time(almoco_in_format.hour + 1, almoco_in_format.minute)
#   lembrete = time(almoco_in_format.hour + 1, almoco_in_format.minute - 1)
#   logfile.write('%s, Entrou na condition da entrada almoco..\n' %(date))
#   date_file_write.write('%s_almoco_in\n' %(today)) # isso aqui est'a l'a no topo..
else:
   almoco_in_format = datetime.strptime(almoco_in, '%H:%M').time()
   retorno_almoco = time(almoco_in_format.hour + 1, almoco_in_format.minute)
   lembrete = time(almoco_in_format.hour + 1, almoco_in_format.minute - 1)
   logfile.write('%s, Entrou na condition da entrada almoco..\n' %(date))
   date_file_write.write('%s_almoco_in\n' %(today))

if '%s_almoco_out' %(today) in date_string and not almoco_out == '--':
   pass
#elif not almoco_out == '--' or not '%s_almoco_out' %(today) in date_string:
#   almoco_in_format = datetime.strptime(almoco_in, '%H:%M').time()
#   retorno_almoco = time(almoco_in_format.hour + 1, almoco_in_format.minute)
#   lembrete = time(almoco_in_format.hour + 1, almoco_in_format.minute - 1)
#   logfile.write('%s, Entrou na condition da saida almoco..\n' %(date))
#   date_file_write.write('%s_almoco_out\n' %(today)) # isso aqui est'a l'a no topo..
else:
   almoco_in_format = datetime.strptime(almoco_in, '%H:%M').time()
   retorno_almoco = time(almoco_in_format.hour + 1, almoco_in_format.minute)
   lembrete = time(almoco_in_format.hour + 1, almoco_in_format.minute - 1)
   logfile.write('%s, Entrou na condition da saida almoco..\n' %(date))
   date_file_write.write('%s_almoco_out\n' %(today)) # isso aqui est'a l'a no topo.. 

# OpenAM logout
querystring = {"_action":"logout"}
headers = {
      'iPlanetDirectoryPro': "%s" %(tokenid['tokenId']),
      'Content-Type': "application/json"
      }
try:
   print("OpenAM Logout..")
   oam_logout = requests.post(sessions, headers=headers, params=querystring, verify=False)
except:
   print("houve algum erro ao tentar fazer logout no OAM..")
   logfile.write('%s ERROR.: OpenAM Logout error..\n' %(date))
   logfile.close()

#close ponto.txt file..
date_file_read.close()
date_file_write.close()

#logs
logfile.close()
