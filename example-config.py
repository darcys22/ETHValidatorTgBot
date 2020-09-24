#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ##### EthValTgBot Config
# Edit starts here
TgBotAPIKey = 'x:y' # API Keythat you get from @BotFather
tg = 1111 # Your id, you can get it by sending command /id to bot @TONTgIDBot

tw = '/var/lib/teku' # validator and beacon work dir

ethvaltgpath = '/home/ubuntu/ethvaltgbot' # User folder with this bot.
ethvaltgpathdb = '/home/ubuntu/ethvaltgbot/db' # User folder with bot database.
# Edit ends here


# Other
elogc = '250' # Row count for the error log
slogc = '250' # Row count for the slow log

srvping = '1.1.1.1' # Ping test server
traceroutetest = '1.1.1.1' # Traceroute test server

nodelogressave = 1 # Save node.log before restart with bot

# Alarms
memloadalarm = 95 # RAM Utilization alarm starts at
pingcalarm = 15 # When ping will be more than X ms, you will get alarm.
cpuutilalarm = 97 # CPU Utilization alarm starts at
timediffalarm = -55 # Time Diff alarm start at
repeattimealarmtd = [5,15,25,30,60,90,120,180,320, 640, 1280, 2560, 5120, 10240, 20480, 40960, 81920] # Notify every x second about time diff check failed
repeattimealarmnode = [5,15,25,30,60,90,120,180,320, 640, 1280, 2560, 5120, 10240, 20480, 40960, 81920] # Notify every x second about validator node down
repeattimealarmsrv = [5,15,25,30,60,90,120,180,320, 640, 1280, 2560, 5120, 10240, 20480, 40960, 81920] # Notify every x second about high CPU, RAM load and ping

# DB Scans
cfgAlertsNotifications = 1 # Validator engine Monitopring
cfgAlertsNotificationsRam = 1 # RAM Monitoring + history
cfgAlertsNotificationsCPU = 1 # CPU Monitoring + history
cfgAlertsNotificationst = 1 # Time Diff Monitopring
cfgmonitoringnetwork = 1 # Netowrk Monitopring
cfgAlertsNotificationsping = 1 # RAM, Ping & CPU Monitopring
cfgmonitoringdiskio = 1 # Disk I/O Monitopring
cfgmonitoringslowlog = 0 # Slow log Monitopring



# ##### /TONTgBot Config
