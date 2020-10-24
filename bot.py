#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import config
import requests
import time
import datetime
import subprocess
import tty
import pty
import psutil
import numpy as np
import pandas as pd
import logging
import threading
import re
import telebot
from telebot import types
from telebot import util
from dotenv import load_dotenv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gettext


# ##### EthValTgBot

# API Token
bot = telebot.TeleBot(config.TgBotAPIKey)
# /API Token

# ##### EthValTgBot

lang_translations = gettext.translation('base', localedir=os.path.join(config.ethvaltgpath, "locales"), languages=['en'])
lang_translations.install()
_ = lang_translations.gettext

# Log
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR) # Outputs Error messages to console.
# /Log

# Menu vars
lt_cpu = _("CPU")
lt_cpu = "\U0001F39B " + lt_cpu
lt_ram = _("RAM")
lt_ram = "\U0001F39A " + lt_ram
lt_disks = _("Disk usage")
lt_disks = "\U0001F4BE " + lt_disks
lt_validatortools = _("Validator tools")
lt_validatortools = "\U0001F48E " + lt_validatortools
lt_linuxtools = _("Linux tools")
lt_linuxtools = "\U0001F9F0 " + lt_linuxtools
#----
lt_ping = _("Ping test")
lt_ping =  "\U0001F3D3 " + lt_ping
lt_traceroute = _("Traceroute test")
lt_traceroute =  "\U0001F9ED " + lt_traceroute
lt_topproc = _("Top processes")
lt_topproc =  "\U0001F51D " + lt_topproc
lt_spdtst = _("Network speed test")
lt_spdtst =  "\U0001F4E1 " + lt_spdtst
lt_currntwrkload = _("Current network load")
lt_currntwrkload =  "\U0001F51B " + lt_currntwrkload
lt_currntdiskload = _("Current disk i/o")
lt_currntdiskload = "\U0001F4BD " + lt_currntdiskload
lt_starttime = _("Uptime")
lt_starttime = "\U0001F7E2 " + lt_starttime
lt_mainmenu = _("Main menu")
lt_mainmenu =  "\U0001F3E1 " + lt_mainmenu
#----
lt_errorsinlogs = _("Error logs")
lt_errorsinlogs =  "\U0001F4D1 " + lt_errorsinlogs
lt_validatorinfomenu = _("Info")
lt_validatorinfomenu =  "\U00002139\U0000FE0F " + lt_validatorinfomenu
lt_slowinlogs = _("Slow logs")
lt_slowinlogs =  "\U0001F422 " + lt_slowinlogs
lt_restartvalidnodee = _("Restart validator")
lt_restartvalidnodee =  "\U0001F504 " + lt_restartvalidnodee
lt_currentstake = _("Current stake")
lt_currentstake =  "\U0001F522 " + lt_currentstake
lt_updatestake = _("Update stake")
lt_updatestake = "\U00002195\U0000FE0F " + lt_updatestake
lt_validatorversion = _("Version")
lt_validatorsyncing = _("Syncing")
lt_validatorhealth  = _("Health")
lt_listvalidator  = _("Validators")
lt_validatorhead  = _("Head")
#---
lt_backlinux =  _("Back to Linux tools")
lt_backlinux = "\U0001F519 " + lt_backlinux
lt_backvalidatorm =  _("Back to Validator tools")
lt_backvalidatorm = "\U0001F519 " + lt_backvalidatorm
# /Menu vars

# Default markup
markup = types.ReplyKeyboardMarkup()
cpu = types.KeyboardButton(lt_cpu)
ram = types.KeyboardButton(lt_ram)
disks = types.KeyboardButton(lt_disks)
currntdiskload = types.KeyboardButton(lt_currntdiskload)
validatortools = types.KeyboardButton(lt_validatortools)
linuxtools = types.KeyboardButton(lt_linuxtools)
markup.row(cpu,ram,disks,currntdiskload)
markup.row(validatortools,linuxtools)
# /Default markup

# Linux markup
markuplinux = types.ReplyKeyboardMarkup()
ping = types.KeyboardButton(lt_ping)
traceroute = types.KeyboardButton(lt_traceroute)
topproc = types.KeyboardButton(lt_topproc)
starttime = types.KeyboardButton(lt_starttime)
spdtst = types.KeyboardButton(lt_spdtst)
currntwrkload = types.KeyboardButton(lt_currntwrkload)
currntdiskload = types.KeyboardButton(lt_currntdiskload)
mainmenu = types.KeyboardButton(lt_mainmenu)
markuplinux.row(ping,traceroute)
markuplinux.row(topproc,starttime,spdtst)
markuplinux.row(currntwrkload,currntdiskload)
markuplinux.row(mainmenu)
# /Linux markup

# Validator markup
markupValidator = types.ReplyKeyboardMarkup()
validatorversion = types.KeyboardButton(lt_validatorversion)
validatorsyncing= types.KeyboardButton(lt_validatorsyncing)
validatorhealth= types.KeyboardButton(lt_validatorhealth)
validatorhead= types.KeyboardButton(lt_validatorhead)
validatorlist= types.KeyboardButton(lt_listvalidator)
mainmenu = types.KeyboardButton(lt_mainmenu)
markupValidator.row(validatorversion,validatorsyncing,validatorhealth,validatorhead)
markupValidator.row(validatorlist)
markupValidator.row(mainmenu)
# /Validator markup

# Validator Info markup
markupValidatorInfo = types.ReplyKeyboardMarkup()
mainmenu = types.KeyboardButton(lt_mainmenu)
backvalidatorm = types.KeyboardButton(lt_backvalidatorm)
markupValidatorInfo.row(backvalidatorm,mainmenu)
# /Validator Info markup

# Get id for tg value
@bot.message_handler(commands=["id"])
def get_id(i):
    id = i.from_user.id
    msg = "Id: " + str(id)
    bot.reply_to(i, msg)
# /Get id for tg value

# Start
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  if message.from_user.id == config.tg:
    bot.send_message(config.tg, _("Hello") + "\U0001F44B\n" + _("I'm here to help you with your Eth2.0 Validator") + " \U0001F9BE\n" + _("Let's choose what you want?"),reply_markup=markup)
  else:
    pass
# /Start

# InlineKeyboards
#CPU
cpuloadhist = types.InlineKeyboardMarkup()
cpuloadhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="cpuhist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="cpuhist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="cpuhist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="cpuhist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="cpuhist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="cpuhist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="cpuhistmore"))

cpuhistmore = types.InlineKeyboardMarkup()
cpuhistmore.row(
types.InlineKeyboardButton(text="\U00002190", callback_data="cpuloadhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="cpuhist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="cpuhist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="cpuhist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="cpuhist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="cpuhist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="cpuhist_30d"))
#CPU

#RAM
ramloadhist = types.InlineKeyboardMarkup()
ramloadhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="ramhist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="ramhist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="ramhist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="ramhist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="ramhist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="ramhist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="ramhistmore"))

ramhistmore = types.InlineKeyboardMarkup()
ramhistmore.row(
types.InlineKeyboardButton(text=_("\U00002190"), callback_data="ramloadhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="ramhist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="ramhist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="ramhist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="ramhist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="ramhist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="ramhist_30d"))
#RAM

# Time Diff
timediffhist = types.InlineKeyboardMarkup()
timediffhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="timediffhist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="timediffhist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="timediffhist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="timediffhist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="timediffhist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="timediffhist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="timediffhistmore"))

timediffhistmore = types.InlineKeyboardMarkup()
timediffhistmore.row(
types.InlineKeyboardButton(text=_("\U00002190"), callback_data="timediffhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="timediffhist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="timediffhist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="timediffhist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="timediffhist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="timediffhist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="timediffhist_30d"))
# Time Diff

#PING
pingcheckhist = types.InlineKeyboardMarkup()
pingcheckhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="pinghist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="pinghist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="pinghist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="pinghist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="pinghist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="pinghist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="pinghistmore"))

pinghistmore = types.InlineKeyboardMarkup()
pinghistmore.row(
types.InlineKeyboardButton(text=_("\U00002190"), callback_data="pingcheckhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="pinghist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="pinghist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="pinghist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="pinghist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="pinghist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="pinghist_30d"))
#PING

# Network
networkcheckhist = types.InlineKeyboardMarkup()
networkcheckhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="networkhist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="networkhist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="networkhist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="networkhist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="networkhist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="networkhist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="networkhistmore"))

networkhistmore = types.InlineKeyboardMarkup()
networkhistmore.row(
types.InlineKeyboardButton(text=_("\U00002190"), callback_data="networkcheckhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="networkhist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="networkhist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="networkhist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="networkhist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="networkhist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="networkhist_30d"))
# Network

# Disk io
diskiocheckhist = types.InlineKeyboardMarkup()
diskiocheckhist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="diskiohist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="diskiohist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="diskiohist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="diskiohist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="diskiohist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="diskiohist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="diskiohistmore"))

diskiohistmore = types.InlineKeyboardMarkup()
diskiohistmore.row(
types.InlineKeyboardButton(text=_("\U00002190"), callback_data="diskiocheckhist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="diskiohist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="diskiohist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="diskiohist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="diskiohist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="diskiohist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="diskiohist_30d"))
# Disk io

# Slow logs events
slowloghist = types.InlineKeyboardMarkup()
slowloghist.row(
types.InlineKeyboardButton(text=_("30m"), callback_data="slowhist_30m"),
types.InlineKeyboardButton(text=_("1h"), callback_data="slowhist_1h"),
types.InlineKeyboardButton(text=_("3h"), callback_data="slowhist_3h"),
types.InlineKeyboardButton(text=_("6h"), callback_data="slowhist_6h"),
types.InlineKeyboardButton(text=_("12h"), callback_data="slowhist_12h"),
types.InlineKeyboardButton(text=_("1d"), callback_data="slowhist_1d"),
types.InlineKeyboardButton(text=_("+"), callback_data="slowhistmore"))

slowhistmore = types.InlineKeyboardMarkup()
slowhistmore.row(
types.InlineKeyboardButton(text="\U00002190", callback_data="slowloghist"),
types.InlineKeyboardButton(text=_("3d"), callback_data="slowhist_3d"),
types.InlineKeyboardButton(text=_("5d"), callback_data="slowhist_5d"),
types.InlineKeyboardButton(text=_("7d"), callback_data="slowhist_7d"),
types.InlineKeyboardButton(text=_("14d"), callback_data="slowhist_14d"),
types.InlineKeyboardButton(text=_("21d"), callback_data="slowhist_21d"),
types.InlineKeyboardButton(text=_("30d"), callback_data="slowhist_30d"))
# Slow logs events

# History load welcome
def historyget(f,t,lbl,ptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=t)
    x = df.iloc[:,0].loc[period]
    y = df.iloc[:,1].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(ptitle)
    plt.yticks(np.arange(0, 100, step=5))
    plt.grid(True)
    plt.ylim(top=100)
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("History load error"))
# History load welcome

# History load welcome Time Diff
def historygettd(f,t,lbl,ptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=t)) & (df.iloc[:,1] < 0)
    x = df.iloc[:,0].loc[period]
    y = df.iloc[:,1].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(ptitle)
    plt.grid(True)
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("History load error"))
# History load welcome Time Diff

# History load welcome Ping
def historygetping(f,t,lbl,ptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=t)
    x = df.iloc[:,0].loc[period]
    y = df.iloc[:,1].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(ptitle)
    plt.grid(True)
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("Ping History load error"))
# History load welcome Ping

# History load welcome Network Bandwidth
def historygetnb(f,t,lbl,dptitle,uptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
    df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
    period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=t)
    x = df.iloc[:,0].loc[period]
    y1 = df.iloc[:,1].loc[period]
    y2 = df.iloc[:,2].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.subplot(2, 1, 1)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(dptitle)
    plt.grid(True)
    plt.plot(x, y1)
    plt.subplot(2, 1, 2)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(uptitle)
    plt.grid(True)
    plt.plot(x, y2)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("Ping History load error"))
# History load welcome Network Bandwidth

# History load welcome Disk I/O
def historygetdio(f,t,lbl,rptitle,wptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    df.iloc[:,1] = df.iloc[:,1]/1024/1024
    df.iloc[:,2] = df.iloc[:,2]/1024/1024
    period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=t)
    x = df.iloc[:,0].loc[period]
    y1 = df.iloc[:,1].loc[period]
    y2 = df.iloc[:,2].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.subplot(2, 1, 1)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(rptitle)
    plt.grid(True)
    plt.plot(x, y1)
    plt.subplot(2, 1, 2)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(wptitle)
    plt.grid(True)
    plt.plot(x, y2)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
# History load welcome Disk I/O

# History load welcome
def historygetslowlog(f,t,lbl,ptitle,poutf,rm):
  try:
    bot.send_chat_action(config.tg, "upload_photo")
    df = pd.read_csv(os.path.join(config.ethvaltgpath, f), sep=";", encoding="utf-8", header=None)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
    period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=t)
    x = df.iloc[:,0].loc[period]
    y = df.iloc[:,2].loc[period]
    plt.figure(figsize=[12, 9], dpi=100)
    plt.xlabel('Time')
    plt.ylabel(lbl)
    plt.title(ptitle)
    plt.grid(True)
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(poutf)
    plt.close()
    load = open(poutf, 'rb')
    bot.send_photo(config.tg, load, reply_markup=rm)
  except:
    bot.send_message(config.tg, text = _("History load error"))
#/History load welcome

# CPU
@bot.message_handler(func=lambda message: message.text == lt_cpu)
def command_cpu(message):
  if message.from_user.id == config.tg:
    try:
      sysload = str(psutil.getloadavg())
      cpuutil = str(psutil.cpu_percent(percpu=True))
      cpu = _("*System load (1,5,15 min):* _") + sysload + _("_\n*CPU utilization %:* _") + cpuutil + "_"
      bot.send_message(config.tg, text=cpu, parse_mode="Markdown")
      historyget("db/cpuload.dat",30,_("Utilization"),_("CPU Utilization"),"/tmp/cpuload.png",cpuloadhist)
    except:
      bot.send_message(config.tg, text=_("Can't get CPU info"))
  else:
    pass
# /CPU

# RAM
@bot.message_handler(func=lambda message: message.text == lt_ram)
def command_ram(message):
  if message.from_user.id == config.tg:
    try:
      ram = _("*RAM, Gb.*\n_Total: ") + str(subprocess.check_output(["free -mh | grep Mem | awk '{print $2}'"], shell = True,encoding='utf-8')) + _("Available: ") + str(subprocess.check_output(["free -mh | grep Mem | awk '{print $7}'"], shell = True,encoding='utf-8')) + _("Used: ") + str(subprocess.check_output(["free -mh | grep Mem | awk '{print $3}'"], shell = True,encoding='utf-8')) + "_"
      swap = _("*SWAP, Gb.*\n_Total: ") + str(subprocess.check_output(["free -mh | grep Swap | awk '{print $2}'"], shell = True,encoding='utf-8')) + _("Available: ") + str(subprocess.check_output(["free -mh | grep Swap | awk '{print $7}'"], shell = True,encoding='utf-8')) + _("Used: ") + str(subprocess.check_output(["free -mh | grep Swap | awk '{print $3}'"], shell = True,encoding='utf-8')) + "_"
      bot.send_message(config.tg, text=ram + swap, parse_mode="Markdown")
      historyget("db/ramload.dat",30,_("Utilization"),_("RAM Utilization"),"/tmp/ramload.png",ramloadhist)
    except:
      bot.send_message(config.tg, text=_("Can't get RAM info"), parse_mode="Markdown")
  else:
    pass
# /RAM

# Disk
@bot.message_handler(func=lambda message: message.text == lt_disks)
def command_disk(message):
  if message.from_user.id == config.tg:
    try:
      disk = str(subprocess.check_output(["df -h -t ext4"], shell = True,encoding='utf-8'))
      dbsize = str(subprocess.check_output(["du -msh " + config.blockchainDB + " | awk '{print $1}'"], shell = True,encoding='utf-8'))
      dbsize = _("*Beaconchain Database size:* _") + dbsize + "_"
      bot.send_message(config.tg, text=dbsize + disk, parse_mode="Markdown", reply_markup=markup)
    except:
      bot.send_message(config.tg, text=_("Can't get disk info"), parse_mode="Markdown", reply_markup=markup)
  else:
    pass
# /Disk

#######################################################
# Validator tools

# Validator tools start
@bot.message_handler(func=lambda message: message.text in (lt_validatortools,lt_backvalidatorm))
def command_linuxtools(message):
    if message.from_user.id == config.tg:
        bot.send_message(config.tg, text= _("Validator Tools"), reply_markup=markupValidator)
    else:
        pass
# /Validator tools start

# Version
@bot.message_handler(func=lambda message: message.text == lt_validatorversion)
def command_errlog(message):
  if message.from_user.id == config.tg:
    try:
        r = requests.get(config.beaconAPI+"/eth/v1/node/version")
        bot.send_message(config.tg, text=r.text, reply_markup=markupValidator)
    except:
        bot.send_message(config.tg, text=_("Can't get Version"), parse_mode="Markdown", reply_markup=markupValidator)
  else:
    pass
# /Version

# Syncing
@bot.message_handler(func=lambda message: message.text == lt_validatorsyncing)
def command_errlog(message):
  if message.from_user.id == config.tg:
    try:
        r = requests.get(config.beaconAPI+"/eth/v1/node/syncing")
        bot.send_message(config.tg, text=r.text, reply_markup=markupValidator)
    except:
        bot.send_message(config.tg, text=_("Can't get Syncing"), parse_mode="Markdown", reply_markup=markupValidator)
  else:
    pass
# /Syncing

# Health
@bot.message_handler(func=lambda message: message.text == lt_validatorhealth)
def command_errlog(message):
  if message.from_user.id == config.tg:
    try:
        r = requests.get(config.beaconAPI+"/eth/v1/node/health")
        bot.send_message(config.tg, text=r.text, reply_markup=markupValidator)
    except:
        bot.send_message(config.tg, text=_("Can't get health"), parse_mode="Markdown", reply_markup=markupValidator)
  else:
    pass
# /Health

# Head
@bot.message_handler(func=lambda message: message.text == lt_validatorhead)
def command_errlog(message):
  if message.from_user.id == config.tg:
    try:
        r = requests.get(config.beaconAPI+"/eth/v1/beacon/headers")
        bot.send_message(config.tg, text=r.text, reply_markup=markupValidator)
    except:
        bot.send_message(config.tg, text=_("Can't get health"), parse_mode="Markdown", reply_markup=markupValidator)
  else:
    pass
# /Head

# Validator List
@bot.message_handler(func=lambda message: message.text == lt_listvalidator)
def command_errlog(message):
  if message.from_user.id == config.tg:
    try:
        r = requests.get(config.validatorAPI+"/lighthouse/validators", headers={'Authorization': 'Basic %s' % config.apitoken})
        bot.send_message(config.tg, text=r.text, reply_markup=markupValidator)
    except:
        bot.send_message(config.tg, text=_("Can't get validator list"), parse_mode="Markdown", reply_markup=markupValidator)
  else:
    pass
# /Validator List

# Validators Info tools
#######################################################

@bot.callback_query_handler(func = lambda call: True)
def inlinekeyboards(call):
  if call.from_user.id == config.tg:
  # CPU graph
    if call.data == "cpuloadhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=cpuloadhist)
    if call.data == "cpuhistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=cpuhistmore)
    if call.data == "cpuhist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_1h = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_1h = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_3h = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_6h = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_12h = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_1d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_1d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuloadhist)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_3d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_3d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_5d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_5d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_7d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_7d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_14d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_14d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_21d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_21d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
    if call.data == "cpuhist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Utilization')
        plt.title('CPU Utilization')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/cpuload.png')
        plt.close()
        cpuload_30d = open('/tmp/cpuload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=cpuload_30d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=cpuhistmore)
        bot.send
      except:
        bot.send_message(config.tg, text = _("CPU Utilization history load error"))
  # CPU graph

  # RAM graph
    if call.data == "ramloadhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=ramloadhist)
    if call.data == "ramhistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=ramhistmore)
    if call.data == "ramhist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_30m = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_30m),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_1h = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_3h = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_6h = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_12h = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_1d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_1d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramloadhist)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_3d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_3d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_5d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_5d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_7d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_7d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_14d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_14d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_21d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_21d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
    if call.data == "ramhist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "ramload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title('RAM Load')
        plt.yticks(np.arange(0, 100, step=5))
        plt.grid(True)
        plt.ylim(top=100)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/ramload.png')
        plt.close()
        ramload_30d = open('/tmp/ramload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=ramload_30d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=ramhistmore)
        bot.send
      except:
        bot.send_message(config.tg, text = _("RAM Load history load error"))
  # RAM graph

  # TimeDiff graph
    if call.data == "timediffhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=timediffhist)
    if call.data == "timediffhistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=timediffhistmore)
    if call.data == "timediffhist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_30m = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_30m),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_1h = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_3h = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_6h = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_12h = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_1d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_1d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhist)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_3d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_3d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_5d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_5d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_7d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_7d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_14d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_14d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_21d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_21d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
    if call.data == "timediffhist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "timediff.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = (df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)) & (df.iloc[:,1] < 0)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Difference')
        plt.title('Time Diff')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/timediff.png')
        plt.close()
        timediff_30d = open('/tmp/timediff.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=timediff_30d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=timediffhistmore)
        bot.send
      except:
        bot.send_message(config.tg, text = _("Time Diff history load error"))
  # TimeDiff graph

  # PING graph
    if call.data == "pingcheckhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=pingcheckhist)
    if call.data == "pinghistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=pinghistmore)
    if call.data == "pinghist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_30m = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_30m),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_1h = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_3h = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_6h = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_12h = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_1d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_1d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pingcheckhist)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_3d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_3d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_5d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_5d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_7d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_7d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_14d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_14d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_21d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_21d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
    if call.data == "pinghist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,1].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('ms')
        plt.title('Ping Check')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/pingcheck.png')
        plt.close()
        pingcheck_30d = open('/tmp/pingcheck.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=pingcheck_30d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=pinghistmore)
        bot.send
      except:
        bot.send_message(config.tg, text = _("Ping check history load error"))
  # PING graph

  # Network graph
    if call.data == "networkcheckhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=networkcheckhist)
    if call.data == "networkhistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=networkhistmore)
    if call.data == "networkhist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_1h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_1h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_3h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_6h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_12h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_24h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_24h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkcheckhist)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_72h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_72h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_120h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_120h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_168h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_168h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_336h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_336h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_504h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_504h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
    if call.data == "networkhist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "networkload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Upload speed')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('Mb/s')
        plt.title('Download speed')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/networkload.png')
        plt.close()
        networkload_720h = open('/tmp/networkload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=networkload_720h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=networkhistmore)
      except:
        bot.send_message(config.tg, text = _("Network Utilization history load error"))
  # Network graph

  # diskio graph
    if call.data == "diskiocheckhist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=diskiocheckhist)
    if call.data == "diskiohistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=diskiohistmore)
    if call.data == "diskiohist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024
        df.iloc[:,2] = df.iloc[:,2]/1024/1024
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_1h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_1h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_3h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_6h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_12h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_24h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_24h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiocheckhist)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_72h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_72h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_120h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_120h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_168h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_168h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_336h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_336h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_504h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_504h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
    if call.data == "diskiohist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        df.iloc[:,1] = df.iloc[:,1]/1024/1024*8
        df.iloc[:,2] = df.iloc[:,2]/1024/1024*8
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y1 = df.iloc[:,1].loc[period]
        y2 = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.subplot(2, 1, 1)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Read')
        plt.grid(True)
        plt.plot(x, y1)
        plt.subplot(2, 1, 2)
        plt.xlabel('Time')
        plt.ylabel('MB/s')
        plt.title('Write')
        plt.grid(True)
        plt.plot(x, y2)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/diskioload.png')
        plt.close()
        diskioload_720h = open('/tmp/diskioload.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=diskioload_720h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=diskiohistmore)
      except:
        bot.send_message(config.tg, text = _("Disk I/O Utilization history load error"))
  # diskio graph

  # SLOW graph
    if call.data == "slowloghist":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=slowloghist)
    if call.data == "slowhistmore":
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=slowhistmore)
    if call.data == "slowhist_30m":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(minutes=30)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[12, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_1h = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_1h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=1)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[15, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_1h = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_1h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_3h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=3)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_3h = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_3h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_6h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=6)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_6h = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_6h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_12h":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=12)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_12h = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_12h),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_1d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=24)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_1d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_1d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowloghist)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_3d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=72)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[20, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_3d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_3d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_5d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=120)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_5d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_5d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_7d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=168)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_7d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_7d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_14d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=336)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_14d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_14d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_21d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=504)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_21d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_21d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
    if call.data == "slowhist_30d":
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], unit='s')
        period = df.iloc[:,0] > df.iloc[:,0].max() - pd.Timedelta(hours=720)
        x = df.iloc[:,0].loc[period]
        y = df.iloc[:,2].loc[period]
        plt.figure(figsize=[30, 9], dpi=100)
        plt.xlabel('Time')
        plt.ylabel('Delay, ms')
        plt.title('Slow events')
        plt.grid(True)
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig('/tmp/slowlog.png')
        plt.close()
        slowlog_30d = open('/tmp/slowlog.png', 'rb')
        bot.edit_message_media(media=types.InputMedia(type='photo', media=slowlog_30d),chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=slowhistmore)
        bot.send
      except:
        bot.send_message(config.tg, text = _("Slow events history load error"))
  # SLOW graph

  # Restart Validator
    if call.data == "res":
      try:
        dorestart = types.InlineKeyboardMarkup()
        dorestart_reply = types.InlineKeyboardButton(text=_("Starting restart process for Validator node"),callback_data="do_restart")
        dorestart.add(dorestart_reply)
        bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=dorestart)
        bot.send_chat_action(config.tg, "typing")
        nodelogbr = str(subprocess.check_output(["du -msh " + config.tw + "/node.log | awk '{print $1}'"], shell = True,encoding='utf-8'))
        nodelogbr = _("*Node.log size before restart :* _") + nodelogbr + "_"
        bot.send_message(config.tg, text = nodelogbr, parse_mode="Markdown")
        bot.send_chat_action(config.tg, "typing")
        killvproc = "ps -eo pid,cmd | grep -i 'validator-engine' | grep -iv 'grep' | awk '{print $1}' | xargs kill -9 $1"
        killvproc = str(subprocess.call(killvproc, shell = True,encoding='utf-8'))
        bot.send_message(config.tg, text = _("Node stopped. RAM & node.log clean. Starting node"), reply_markup=markupValidator)
        bot.send_chat_action(config.tg, "typing")
        time.sleep(1)
        if config.nodelogressave == 1:
          tms = str(datetime.datetime.today().strftime("%b_%d_%Y-%H_%M_%S"))
          nodelogsavelog = str(subprocess.call(["mv " + config.tw + "/node.log " + config.tw + "/node_before_" + tms + ".log"], shell = True,encoding='utf-8'))
        else:
          pass
        time.sleep(3)
        try:
          master, slave = pty.openpty()
          stdout = None
          stderr = None
          #runvproc = config.ethvaltgpath + "/run.sh"
          runvproc = "/bin/bash " + config.tf + "scripts/run.sh"
          runvprocc = subprocess.Popen(runvproc, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8', close_fds=True)
          stdout, stderr = runvprocc.communicate(timeout=5)
          os.close(slave)
          os.close(master)
          bot.send_message(config.tg, text = stdout, reply_markup=markupValidator)
        except Exception as i:
          kill(runvprocc.pid)
          os.close(slave)
          os.close(master)
          bot.send_message(config.tg, text = _("Start error. Try to start your node manually"), reply_markup=markupValidator)
      except:
        bot.send_message(config.tg, text = _("Restart error. Try to restart your node manually"), reply_markup=markupValidator)
    if call.data == "nores":
      norestart = types.InlineKeyboardMarkup()
      norestart_reply = types.InlineKeyboardButton(text=_("Declined"),callback_data="no_exit")
      norestart.add(norestart_reply)
      bot.edit_message_reply_markup(config.tg, message_id=call.message.message_id, reply_markup=norestart)
  else:
    pass
@bot.message_handler(func=lambda message: message.text == lt_restartvalidnodee)
# Restart validator node
def command_restartvalidator(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      restartkbd = types.InlineKeyboardMarkup()
      restartvalidnod_1 = types.InlineKeyboardButton(text=_("Restart node"), callback_data="res")
      restartkbd.add(restartvalidnod_1)
      restartvalidnod_0 = types.InlineKeyboardButton(text=_("Don't restart the node"), callback_data="nores")
      restartkbd.add(restartvalidnod_0)
      bot.send_message(config.tg, text = _("Do you really want to restart validator node?"), reply_markup=restartkbd)
    except:
      bot.send_message(config.tg, text = _("Restart error"))
  else:
    pass
# /Restart validator node

# Current stake
@bot.message_handler(func=lambda message: message.text == lt_currentstake)
def command_currentstake(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      currentstake = "crontab -l | grep -oP 'validator_msig.sh ([0-9]+)' | awk '{print $2}'"
      currentstake = str(subprocess.check_output(currentstake, shell = True,encoding='utf-8').rstrip())
      bot.send_message(config.tg, text = _("Your current stake is ") + currentstake + " \U0001F48E", reply_markup=markupValidator)
    except:
      bot.send_message(config.tg, text = _("Can't get current stake"), reply_markup=markupValidator)
  else:
    pass
# /Current stake

# Update stake
@bot.message_handler(func=lambda message: message.text == lt_updatestake)
def command_updatestake(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      uddatestake = "crontab -l | grep -oP 'validator_msig.sh ([0-9]+)' | awk '{print $2}'"
      uddatestake = str(subprocess.check_output(uddatestake, shell = True,encoding='utf-8').rstrip())
      bot.send_message(config.tg, text = _("Your current stake ") + uddatestake + " \U0001F48E \n" + _("To update your current stake, please send me command /updstake 10001, where 10001 is your new stake "), reply_markup=markupValidator)
    except:
      bot.send_message(config.tg, text = _("Update stake command error"), reply_markup=markupValidator)
  else:
    pass
# /Update stake

# Update stake command
@bot.message_handler(commands=["updstake"])
def send_welcome(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      stakesize = message.text.split()
      stakesize = str(int(stakesize[1]))
      updatestakecmd = "crontab -l | sed 's/validator_msig.sh \([0-9]\+\)/validator_msig.sh " + stakesize + "/' | crontab -"
      updatestakecmd = str(subprocess.call(updatestakecmd, shell = True,encoding='utf-8'))
      time.sleep(1)
      currentstake = "crontab -l | grep -oP 'validator_msig.sh ([0-9]+)' | awk '{print $2}'"
      currentstake = str(subprocess.check_output(currentstake, shell = True,encoding='utf-8').rstrip())
      bot.send_message(config.tg, text = _("Your NEW stake: ") + currentstake + " \U0001F48E", reply_markup=markupValidator)
    except:
      try:
        currentstake = "crontab -l | grep -oP 'validator_msig.sh ([0-9]+)' | awk '{print $2}'"
        bot.send_message(config.tg, text = _("Update ERROR. Your current stake is ") + currentstake + " \U0001F48E", reply_markup=markupValidator)
      except:
        bot.send_message(config.tg, text = _("Update ERROR"), reply_markup=markupValidator)
  else:
    pass
# /Update stake command

# /Validator tools
#######################################################


#######################################################
# Linux tools

# Linux tools start
@bot.message_handler(func=lambda message: message.text == lt_linuxtools)
def command_linuxtools(message):
  if message.from_user.id == config.tg:
    bot.send_message(config.tg, text=_("Be careful. Some processes need time. ") + "\U000023F3", reply_markup=markuplinux)
  else:
    pass
# /Linux tools start

# Ping test
@bot.message_handler(func=lambda message: message.text == lt_ping)
def command_pingcheck(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      pingcheck = "ping -c 5 " + config.srvping
      pingcheck = str(subprocess.check_output(pingcheck, shell = True,encoding='utf-8'))
      bot.send_message(config.tg, text=pingcheck, reply_markup=markuplinux)
      historygetping("db/pingcheck.dat",30,_("ms"),_("Ping test"),"/tmp/pingcheck.png",pingcheckhist)
    except:
      bot.send_message(config.tg, text=_("Can't execute ping test"), reply_markup=markuplinux)
  else:
    pass
# /Ping test

# Traceroute test
@bot.message_handler(func=lambda message: message.text == lt_traceroute)
def command_traceroutecheck(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      bot.send_chat_action(config.tg, "typing")
      traceroutecheck = "traceroute -4 -w 3 " + config.traceroutetest
      traceroutecheck = str(subprocess.check_output(traceroutecheck, shell = True,encoding='utf-8'))
      bot.send_message(config.tg, text=traceroutecheck, reply_markup=markuplinux)
    except:
      bot.send_message(config.tg, text=_("Can't execute tracerote command"), reply_markup=markuplinux)
  else:
    pass
# /Traceroute test

# Top processes
@bot.message_handler(func=lambda message: message.text == lt_topproc)
def command_timediff(message):
  if message.from_user.id == config.tg:
    try:
      topps = "ps -eo pid,ppid,user,start,%mem,pcpu,cmd --sort=-%mem | head"
      topps = str(subprocess.check_output(topps, shell = True,encoding='utf-8'))
      bot.send_message(config.tg, text=topps, reply_markup=markuplinux)
    except:
      bot.send_message(config.tg, text=_("Can't get top processes"), reply_markup=markuplinux)
  else:
    pass
# /Top processes

# Server start date/time
@bot.message_handler(func=lambda message: message.text == lt_starttime)
def command_srvstart(message):
  if message.from_user.id == config.tg:
    try:
      startt = _("System start: ") + str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%b/%d/%Y %H:%M:%S"))
      bot.send_message(config.tg, text=startt, reply_markup=markuplinux)
    except:
      bot.send_message(config.tg, text=_("Can't get system start date"), reply_markup=markuplinux)
  else:
    pass
# /Server start date/time

# Current network load
@bot.message_handler(func=lambda message: message.text == lt_currntwrkload)
def command_currntwrkload(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      currentloadn = psutil.net_io_counters()
      bytes_sent = getattr(currentloadn, 'bytes_sent')
      bytes_recv = getattr(currentloadn, 'bytes_recv')
      time.sleep(1)
      currentloadn1 = psutil.net_io_counters()
      bytes_sent1 = getattr(currentloadn1, 'bytes_sent')
      bytes_recv1 = getattr(currentloadn1, 'bytes_recv')
      sentspd = (bytes_sent1-bytes_sent)/1024/1024*8
      recvspd = (bytes_recv1-bytes_recv)/1024/1024*8
      sentspd = str((round(sentspd, 2)))
      recvspd = str((round(recvspd, 2)))
      bot.send_message(config.tg, text=_("*Current network load\nIncoming:* _") + recvspd + _(" Mb/s_\n*Outgoing:* _") + sentspd + _(" Mb/s_"), parse_mode="Markdown", reply_markup=markuplinux)
      historygetnb("db/networkload.dat",0.5,_("Mb/s"),_("Upload"),_("Download"),"/tmp/networkload.png",networkcheckhist)
    except:
      bot.send_message(config.tg, text=_("Can't get current network load"), parse_mode="Markdown", reply_markup=markuplinux)
  else:
    pass
# /Current network load

# Disk I/O
@bot.message_handler(func=lambda message: message.text == lt_currntdiskload)
def command_currdiskload(message):
  if message.from_user.id == config.tg:
    try:
      bot.send_chat_action(config.tg, "typing")
      currentloadd = psutil.disk_io_counters()
      bytes_read = getattr(currentloadd, 'read_bytes')
      bytes_writ = getattr(currentloadd, 'write_bytes')
      time.sleep(1)
      currentloadd1 = psutil.disk_io_counters()
      bytes_read1 = getattr(currentloadd1, 'read_bytes')
      bytes_writ1 = getattr(currentloadd1, 'write_bytes')
      readio = (bytes_read1-bytes_read)/1024/1024
      writio = (bytes_writ1-bytes_writ)/1024/1024
      readio = str((round(readio, 2)))
      writio = str((round(writio, 2)))
      bot.send_message(config.tg, text=_("*Current disk load\nRead:* _") + readio + _(" MB/s_\n*Write:* _") + writio + _(" MB/s_"), parse_mode="Markdown")
      historygetdio("db/diskioload.dat",0.5,_("MB/s"),_("Read"),_("Write"),"/tmp/diskioload.png",diskiocheckhist)
    except:
      bot.send_message(config.tg, text=_("Can't get current disk load"), parse_mode="Markdown")
  else:
    pass
# /Disk I/O

# /Linux tools
#######################################################



#######################################################
# Network speed tool

# Network speed start
@bot.message_handler(func=lambda message: message.text == lt_spdtst)
def command_speedtest(message):
    if message.from_user.id == config.tg:
        try:
            bot.send_chat_action(config.tg, "typing")
            testspeedcmd = "python3 " + config.ethvaltgpath + "/speedtest-cli --share | grep -i 'Share results' | awk '{print $3}' | wget -i - -O /tmp/speedtestcheck.png"
            testspeed =str(subprocess.call(testspeedcmd, shell = True,encoding='utf-8'))
            bot.send_chat_action(config.tg, "upload_photo")
            testspeedfile = open('/tmp/speedtestcheck.png', 'rb')
            bot.send_photo(config.tg, testspeedfile, reply_markup=markuplinux)
        except:
            bot.send_message(config.tg, text=_("Network speed test check failed"), reply_markup=markuplinux)
    else:
        pass
# Network speed start


# Back to linux tools
@bot.message_handler(func=lambda message: message.text == lt_backlinux)
def command_backtolinux(message):
  if message.from_user.id == config.tg:
    bot.send_message(config.tg, text=_("Be careful. Some processes need time ") + " \U000023F3", reply_markup=markuplinux)
  else:
    pass
# /Back to linux tools

# Network speed tool
#######################################################


# Main menu
@bot.message_handler(func=lambda message: message.text == lt_mainmenu)
def command_srvstart(message):
  if message.from_user.id == config.tg:
    bot.send_message(config.tg, text=_("Start menu"), reply_markup=markup)
  else:
    pass
# /Main menu

# Except proc kill
def kill(proc_pid):
  process = psutil.Process(proc_pid)
  for proc in process.children(recursive=True):
    proc.kill()
  process.kill()

# Alerts Validator node
def AlertsNotifications():
  td = 0
  hch = 0
  t,p,c = 5,2,15
  #q = [t * p ** (i - 1) for i in range(1, c + 1)]

  alrtprdvnr = 5
  while True:
    if td == 5:
      td = 0

      # Check validator node running
      # try:
        # valnodecheck = str(subprocess.check_output(["pidof", "validator-engine"], encoding='utf-8'))
        # alrtprdvnr =5
      # except subprocess.CalledProcessError as i:
        # if i.output != None:
          # if alrtprdvnr in config.repeattimealarmnode:
            # try:
              # bot.send_message(config.tg, text="\U0001F6A8 " + _("Validator node is not running!!! Restart node in process."),  parse_mode="Markdown", reply_markup=markupValidator)
              # bot.send_chat_action(config.tg, "typing")
              # nodelogbr = str(subprocess.check_output(["du -msh " + config.tw + "/node.log | awk '{print $1}'"], shell = True,encoding='utf-8'))
              # nodelogbr = _("*Node.log size before restart :* _") + nodelogbr + "_"
              # bot.send_message(config.tg, text = nodelogbr, parse_mode="Markdown")
              # bot.send_chat_action(config.tg, "typing")
              # killvproc = "ps -eo pid,cmd | grep -i 'validator-engine' | grep -iv 'grep' | awk '{print $1}' | xargs kill -9 $1"
              # killvproc = str(subprocess.call(killvproc, shell = True,encoding='utf-8'))
              # bot.send_message(config.tg, text = _("Node stopped. RAM & node.log clean. Starting node"), reply_markup=markupValidator)
              # bot.send_chat_action(config.tg, "typing")
              # time.sleep(1)
              # if config.nodelogressave == 1:
                # tms = str(datetime.datetime.today().strftime("%b_%d_%Y-%H_%M_%S"))
                # nodelogsavelog = str(subprocess.call(["mv " + config.tw + "/node.log " + config.tw + "/node_before_" + tms + ".log"], shell = True,encoding='utf-8'))
              # else:
                # pass
              # time.sleep(2)
              # try:
                # master, slave = pty.openpty()
                # stdout = None
                # stderr = None
                # #runvproc = config.ethvaltgpath + "/run.sh"
                # runvproc = "/bin/bash " + config.tf + "scripts/run.sh"
                # runvprocc = subprocess.Popen(runvproc, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8', close_fds=True)
                # stdout, stderr = runvprocc.communicate(timeout=5)
                # os.close(slave)
                # os.close(master)
                # bot.send_message(config.tg, text = stdout, reply_markup=markupValidator)
              # except Exception as i:
                # kill(runvprocc.pid)
                # os.close(slave)
                # os.close(master)
                # bot.send_message(config.tg, text = _("Start error. Try to start your node manually"), reply_markup=markupValidator)
            # except:
              # bot.send_message(config.tg, text = _("Restart error. Try to restart your node manually"), reply_markup=markupValidator)
            # alrtprdvnr +=5
          # else:
            # alrtprdvnr +=5
    hch += 5
    time.sleep(5)
    td += 5
#




def AlertsNotificationst():

  td = 0
  t,p,c = 5,2,15
  #q = [t * p ** (i - 1) for i in range(1, c + 1)]

  alrtprdtdf = 5
  while True:
    if td == 5:
      td = 0
      # try:
        # master, slave = pty.openpty()
        # stdout = None
        # stderr = None
        # timediffcmd = "/bin/bash " + config.tf + "scripts/check_node_sync_status.sh | grep TIME_DIFF | awk '{print $4}'"
        # timediff = subprocess.Popen(timediffcmd, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8', close_fds=True)
        # stdout, stderr = timediff.communicate(timeout=2)
        # os.close(slave)
        # os.close(master)
        # with open(os.path.join(config.ethvaltgpathdb, "timediff.dat"), "a") as i:
          # i.write(str(int(time.time())) + ";" + stdout.rstrip() + "\n")
        # if int(stdout) < config.timediffalarm:
          # if alrtprdtdf in config.repeattimealarmtd:
            # try:
              # bot.send_message(config.tg, text=_("Time Diff is ") + stdout)
            # except:
              # pass
            # alrtprdtdf +=5
          # else:
            # alrtprdtdf +=5
        # if int(stdout) >= config.timediffalarm:
          # alrtprdtdf = 5
      # except Exception as i:
        # kill(timediff.pid)
        # os.close(slave)
        # os.close(master)
        # if i.output == None:
          # if alrtprdtdf in config.repeattimealarmtd:
            # try:
              # bot.send_message(config.tg, text=_("Time Diff check failed"), reply_markup=markupValidator)
            # except:
              # pass
            # alrtprdtdf +=5
          # else:
            # alrtprdtdf +=5
    else:
      time.sleep(5)
      td += 5

# Alerts Validator node

# RAM Monitoring
def AlertsNotificationsRam():
  td = 0
  alrtprdmem = 5
  while True:
    if td == 5:
      try:
        td = 0
        memload = "free -m | grep Mem | awk '/Mem/{used=$3} /Mem/{total=$2} END {printf (used*100)/total}'"
        memload = str(subprocess.check_output(memload, shell = True, encoding='utf-8'))
        # History data
        with open(os.path.join(config.ethvaltgpathdb, "ramload.dat"), "a") as i:
          i.write(str(int(time.time())) + ";" + memload + "\n")
        # Notification
        if int(float(memload)) >= config.memloadalarm:
          if alrtprdmem in config.repeattimealarmsrv:
            try:
              bot.send_message(config.tg, text="\U0001F6A8 " + _("High memory load!!! ") + memload + _("% I recommend you to restart your *validator* node "),  parse_mode="Markdown")
            except:
              pass
            alrtprdmem +=5
          else:
            alrtprdmem +=5
        if int(float(memload)) < config.memloadalarm:
          alrtprdmem = 5
        time.sleep(5)
        td += 5
      except:
        time.sleep(5)
        td += 5
    else:
      time.sleep(5)
      td += 5

# CPU Monitoring
def AlertsNotificationsCPU():
  td = 0
  alrtprdcpu = 5
  while True:
    if td == 5:
      try:
        td = 0
        cpuutilalert = str(psutil.cpu_percent())
        with open(os.path.join(config.ethvaltgpathdb, "cpuload.dat"), "a") as i:
          i.write(str(int(time.time())) + ";" + cpuutilalert + "\n")
        if int(float(cpuutilalert)) >= config.cpuutilalarm:
          if alrtprdcpu in config.repeattimealarmsrv:
            try:
              bot.send_message(config.tg,"\U000026A1" + _("High CPU Utilization! ") + cpuutilalert + "%")
            except:
              pass
            alrtprdcpu +=5
          else:
            alrtprdcpu +=5
        if int(float(cpuutilalert)) < config.cpuutilalarm:
          alrtprdcpu = 5
        time.sleep(5)
        td += 5
      except:
        time.sleep(5)
        td += 5
    else:
      time.sleep(5)
      td += 5




def AlertsNotificationsping():
  td = 0
  alrtprdpng = 5
  while True:
    if td == 5:
      try:
        td = 0
        pingc = "ping -c 1 " + config.srvping + " | tail -1 | awk '{printf $4}' | cut -d '/' -f 1 | tr -d $'\n'"
        pingc = str(subprocess.check_output(pingc, shell = True, encoding='utf-8'))
        with open(os.path.join(config.ethvaltgpathdb, "pingcheck.dat"), "a") as i:
          i.write(str(int(time.time())) + ";" + pingc + "\n")
        if int(float(pingc)) >= config.pingcalarm:
          if alrtprdpng in config.repeattimealarmsrv:
            try:
              bot.send_message(config.tg,"\U000026A1 " + _("High ping! ") + pingc + " ms")
            except:
              pass
            alrtprdpng +=5
          else:
            alrtprdpng +=5
        if int(float(pingc)) < config.pingcalarm:
          alrtprdpng = 5
        time.sleep(5)
        td += 5
      except:
        time.sleep(5)
        td += 5
    else:
      time.sleep(5)
      td += 5



def monitoringnetwork():
  td = 0
  while True:
    if td == 5:
      td = 0
      try:
        currentloadn = psutil.net_io_counters()
        bytes_sent = getattr(currentloadn, 'bytes_sent')
        bytes_recv = getattr(currentloadn, 'bytes_recv')
        time.sleep(1)
        currentloadn1 = psutil.net_io_counters()
        bytes_sent1 = getattr(currentloadn1, 'bytes_sent')
        bytes_recv1 = getattr(currentloadn1, 'bytes_recv')
        sentspd = (bytes_sent1-bytes_sent)
        recvspd = (bytes_recv1-bytes_recv)
        with open(os.path.join(config.ethvaltgpathdb, "networkload.dat"), "a") as i:
          i.write(str(int(time.time())) + ";" + str(int(sentspd)) + ";" + str(int(recvspd)) + "\n")
      except:
        pass
    else:
      time.sleep(4)
      td += 5

def monitoringdiskio():
  td = 0
  while True:
    if td == 5:
      td = 0
      try:
        currentloadd = psutil.disk_io_counters()
        bytes_read = getattr(currentloadd, 'read_bytes')
        bytes_writ = getattr(currentloadd, 'write_bytes')
        time.sleep(1)
        currentloadd1 = psutil.disk_io_counters()
        bytes_read1 = getattr(currentloadd1, 'read_bytes')
        bytes_writ1 = getattr(currentloadd1, 'write_bytes')
        readio = (bytes_read1-bytes_read)
        writio = (bytes_writ1-bytes_writ)
        readio = str((round(readio, 2)))
        writio = str((round(writio, 2)))
        with open(os.path.join(config.ethvaltgpathdb, "diskioload.dat"), "a") as i:
          i.write(str(int(time.time())) + ";" + str(int(readio)) + ";" + str(int(writio)) + "\n")
      except:
        pass
    else:
      time.sleep(4)
      td += 5

def monitoringslowlog():
  td = 0
  while True:
    if td == 300:
      td = 0
      try:
        df = pd.read_csv(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), sep=";", encoding="utf-8", header=None)
        last_slow = int(df.iloc[-1:,0])
        with open(os.path.join(config.tw, "node.log"), 'r') as fl:
          for line in fl:
            re_date = re.findall(r'(\d{10})(?:\.\d{9})(?:.*)',line)
            try:
              re_date = ("".join(re_date[0]))
              if int(re_date) > last_slow:
                re_slow = re.findall(r'(\d{10}\.\d{9})(?:.*)\bSLOW(?:.*)\bname:(\w+)(?:.*)\bduration:(\d+)',line)
                if len(re_slow) == 1:
                  re_slow = (";".join(re_slow[0]))
                  with open(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), 'a') as sla:
                    sla.write(str(re_slow) + '\n')
                else:
                  pass
              else:
                pass
            except:
              pass
      except FileNotFoundError:
        with open(os.path.join(config.tw, "node.log"), 'r') as fl:
          for line in fl:
            re_slow = re.findall(r'(\d{10}\.\d{9})(?:.*)\bSLOW(?:.*)\bname:(\w+)(?:.*)\bduration:(\d+)',line)
            try:
              if len(re_slow) == 1:
                re_slow = (";".join(re_slow[0]))
                with open(os.path.join(config.ethvaltgpathdb, "slowlog.dat"), 'a') as sla:
                  sla.write(str(re_slow) + '\n')
              else:
                  pass
            except:
              pass
      except:
        pass
    else:
      time.sleep(300)
      td += 300

if __name__ == '__main__':

  if config.cfgAlertsNotifications == 1:
    AlertsNotifications = threading.Thread(target = AlertsNotifications)
    AlertsNotifications.start()

  if config.cfgAlertsNotificationsRam == 1:
    AlertsNotificationsRam = threading.Thread(target = AlertsNotificationsRam)
    AlertsNotificationsRam.start()

  if config.cfgAlertsNotificationsCPU == 1:
    AlertsNotificationsCPU = threading.Thread(target = AlertsNotificationsCPU)
    AlertsNotificationsCPU.start()

  if config.cfgAlertsNotificationst == 1:
    AlertsNotificationst = threading.Thread(target = AlertsNotificationst)
    AlertsNotificationst.start()

  if config.cfgmonitoringnetwork == 1:
    monitoringnetwork = threading.Thread(target = monitoringnetwork)
    monitoringnetwork.start()

  if config.cfgAlertsNotificationsping == 1:
    AlertsNotificationsping = threading.Thread(target = AlertsNotificationsping)
    AlertsNotificationsping.start()

  if config.cfgmonitoringdiskio == 1:
    monitoringdiskio = threading.Thread(target = monitoringdiskio)
    monitoringdiskio.start()

  if config.cfgmonitoringslowlog == 1:
    monitoringslowlog = threading.Thread(target = monitoringslowlog)
    monitoringslowlog.start()

  else:
    pass





while True:
  try:
    bot.polling(none_stop=True, timeout=10) #constantly get messages from Telegram
  except:
    bot.stop_polling()
    time.sleep(5)
