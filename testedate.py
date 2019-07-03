#!/bin/usr/env python
from datetime import datetime, timedelta, time
import sys
from auth_portal import entrada, almoco_in, almoco_out, oam_logout

#entrada = '10:34'
#saida_almoco = '13:04'
#retorno_almoco = '14:04'

_entrada = entrada
saida_almoco = almoco_in
retorno_almoco = almoco_out

if _entrada == '--' and saida_almoco == '--' and retorno_almoco == '--':
   sys.exit(0)
if saida_almoco == '--':
   print('no lunch marking - almoco_in')
   if retorno_almoco == '--':
      print('no lunch marking - almoco_out')
      sys.exit(0)

# transformando..
srtf_entrada = datetime.strptime(_entrada, '%H:%M').time()
srtf_saida_almoco = datetime.strptime(saida_almoco, '%H:%M').time()

#precisao de retorno almoco caso ainda nao batido.
if retorno_almoco == '--':
   retorno_almoco = time(srtf_saida_almoco.hour + 1, srtf_saida_almoco.minute)
   srtf_retorno_almoco = '%s' %(retorno_almoco.strftime('%H:%M')) 
   string_retorno_almoco = '%s' %(srtf_retorno_almoco)
   campos_retorno_almoco = string_retorno_almoco.split(':')
   retorno_almoco_hora = campos_retorno_almoco[0]
   retorno_almoco_minuto = campos_retorno_almoco[1]

else:
   srtf_retorno_almoco = datetime.strptime(retorno_almoco, '%H:%M').time()
   string_retorno_almoco = '%s' %(srtf_retorno_almoco)
   campos_retorno_almoco = string_retorno_almoco.split(':')
   retorno_almoco_hora = campos_retorno_almoco[0]
   retorno_almoco_minuto = campos_retorno_almoco[1]
   retorno_almoco_segundo = campos_retorno_almoco[2]

#if not retorno_almoco == '--':
#   srtf_retorno_almoco = datetime.strptime(retorno_almoco, '%H:%M').time()
#   string_retorno_almoco = '%s' %(srtf_retorno_almoco)
#   campos_retorno_almoco = string_retorno_almoco.split(':')
#   retorno_almoco_hora = campos_retorno_almoco[0]
#   retorno_almoco_minuto = campos_retorno_almoco[1]
#   retorno_almoco_segundo = campos_retorno_almoco[2]

# horario entrada formatando...
string_entrada = '%s' %(srtf_entrada)
campos_entrada = string_entrada.split(':')
entrada_hora = campos_entrada[0]
entrada_minuto = campos_entrada[1]
entrada_segundo = campos_entrada[2]

# horario saida almoco formatando...
string_saida_almoco = '%s' %(srtf_saida_almoco)
campos_saida_almoco = string_saida_almoco.split(':')
saida_almoco_hora = campos_saida_almoco[0]
saida_almoco_minuto = campos_saida_almoco[1]
saida_almoco_segundo = campos_saida_almoco[2]

if int(entrada_minuto) == 12 and int(saida_almoco_minuto) == int(retorno_almoco_minuto) or int(entrada_minuto) < 12 and int(retorno_almoco_minuto) == 12:
   entrada_minuto_soma = 0
   entrada_hora_soma = int(entrada_hora) + 10
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-1: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))

elif int(entrada_minuto) < 12 and int(saida_almoco_minuto) == int(retorno_almoco_minuto):
   entrada_minuto_soma = 48 + int(entrada_minuto)
   entrada_hora_soma = int(entrada_hora) + 9
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-2: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))

elif int(entrada_minuto) <= 7 and int(retorno_almoco_minuto) <= 4 or int(entrada_minuto) <= 4 and int(retorno_almoco_minuto) <= 7:
   entrada_minuto_soma = int(retorno_almoco_minuto) + 48 + int(entrada_minuto)
   entrada_hora_soma = int(entrada_hora) + 9
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-3: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))

elif int(entrada_minuto) <= 12 and int(saida_almoco_minuto) < int(retorno_almoco_minuto):
   entrada_minuto_soma = int(entrada_minuto) + 48 + ( int(retorno_almoco_minuto) - int(saida_almoco_minuto) ) - 60
   entrada_hora_soma = int(entrada_hora) + 9 if int(entrada_minuto) < 1 else int(entrada_hora) + 10
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-4: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))

elif int(entrada_minuto) > 12 and int(saida_almoco_minuto) < int(retorno_almoco_minuto):
   entrada_minuto_soma = int(entrada_minuto) + 48 + ( int(retorno_almoco_minuto) - int(saida_almoco_minuto) ) - 60
   entrada_hora_soma = int(entrada_hora) + 9 if int(entrada_minuto) < 1 else int(entrada_hora) + 10
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-5: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))

else:
   entrada_minuto_soma = int(entrada_minuto) + 48 - 60
   entrada_hora_soma = int(entrada_hora) + 9 if int(entrada_minuto) < 1 else int(entrada_hora) + 10
   if len(str(entrada_minuto_soma)) == 1:
      saida_prevista = '%s:0%s' %(entrada_hora_soma, entrada_minuto_soma)
   else:
      saida_prevista = '%s:%s' %(entrada_hora_soma, entrada_minuto_soma)
   print("condicao-6: {}:{}".format(entrada_hora_soma, entrada_minuto_soma))
