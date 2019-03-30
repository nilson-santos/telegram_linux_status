#!/usr/bin/python3
import json, math, telepot
from uptime       import uptime
from subprocess   import call, check_output

#enter your json path below with constant and bot information
autht_path = '/home/auth.json'

def temp():
    res = check_output('vcgencmd measure_temp', shell=True)
    return(res.decode()).replace('temp=',' ').replace("'C","°C🌡")

def cpu():
    disk = check_output("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True)
    return(str(disk)).replace("b","").replace("'","")

def mem():
    mem = check_output("free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell=True)
    return(str(mem)).replace("b","").replace("'","")

def disk():
    disk = check_output("df -h | awk '$NF==\"/\"{printf \"%.1f/%.1fGB %s\", $3,$2,$5}'", shell=True)
    return(str(disk)).replace("b","").replace("'","")

def uptm():
    if math.floor(uptime() / 60) < 2:
        tm = (str(math.floor(uptime() / 60)) + ' minute')

    elif math.floor(uptime() / 60) >= 2 and math.floor(uptime() / 60) < 60:
        tm = (str(math.floor(uptime() / 60)) + ' minutes')

    elif math.floor(uptime() / 60) >= 60 and math.floor(uptime() / 60) < 120:
        tm = (str(math.floor(uptime() / 3600)) + ' hour')

    elif math.floor(uptime() / 60) >= 120 and math.floor(uptime() / 86400) < 1:
        tm = (str(math.floor(uptime() / 3600)) + ' hours')

    elif math.floor(uptime() / 86400) >= 1 and math.floor(uptime() / 86400) < 2:
        tm = (str(math.floor(uptime() / 86400)) + ' day')

    else:
        tm = (str(math.floor(uptime() / 86400)) + ' days')

    return(tm)

def porta():
    call('curl -4 ifconfig.co/port/22 > /home/pi/porta.txt', shell=True)
    with open('/home/pi/porta.txt') as file:
        ifconfig = json.load(file)
        ip = ifconfig['ip']

        if ifconfig['reachable'] == True:
            estado = '\n*Firewall:* Disable ⛔'
        else:
            estado = '\n*Firewall:* Enable ✅'

        call('rm /home/pi/porta.txt &', shell=True)

    return(ip, estado)


ip, estado = porta()

with open(autht_path) as file:
    secrets = json.load(file)

    bot = telepot.Bot(secrets['tg_tk_bot'])
    tg_destiny = secrets['tg_id_to']

bot.sendMessage(tg_destiny, '*CPU Temp:*' + temp() + '*Uptime:* ' \
				 + uptm() + "\n*IP:* " + ip + '\n*CPU Load:* ' + cpu() + '\n*Mem:* '\
                 + mem() + '\n*Disk:* ' + disk() + estado, parse_mode='Markdown')