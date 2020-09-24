# EthValTgBot Readme
This is telegram bot for your Validator. 

This bot can only send messages to your telegram id

## What this bot can do?

####  Monitoring

 1. Validator node + Automatic restart if node down
 2. CPU load 
 3. RAM load
 4. Network
 5. Time diff
 6. Wallet balance
 7. Stake monitoring + Auto stake (New!)
 8. Error log monitoring
 9. Slow log monitoring
 10. Stake send check (New!)

#### Historical data
 1. CPU Utilization
 2. RAM Load
 3. Time Diff
 4. Slow log events
 5. Disk I/O
 6. Network perfomance 
 7. Ping test 

#### Alert

 1. Validator node down
 2. High CPU Utilization
 3. High RAM load
 4. Network degradation
 5. Stake < Wallet balance
 6. Stake not send check (New!)

## Installation in 5 simple steps (2-3 minutes, and your bot is ready)

 1. Create your personal telegram bot and get Api Token. [Instruction](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0)
 2. Send to your new bot command /start and go to the next step
 3. Run command below
```sh
$ cd $HOME && git clone -v https://github.com/darcys22/EthValTgBot.git ethvaltgbot && cd ./ethvaltgbot && chmod +x ./installsbot.sh
```
 4. Open ./config.py in any editor and change values from *Edit starts here* till *Edit ends here*. If you dont know your id(tg value), Just send message to @TONTgIDBot in telegram. Then open ./sbot.sh and put user folder at lines 14-15. Open ./tontgbot.service and put user&group at lines 7-8
 
 5. Run 
 ```sh
$ /bin/bash ./installsbot.sh
```

## Available languages *Yes, with google translate
Change languages=['en'] in bot.py to language, what you need
  ```sh
lang_translations = gettext.translation('base', localedir='/opt/tontgbot/locales', languages=['en'])
```

Language - code
* English - en
* Español - es
* Français - fr
* Dansk - da
* Nederlands - nl
* हिंदी - hi
* Italiano - it
* Polski - pl
* Português - pt
* Suomi - fi
* Svenska - sv
* Türkçe - tr
* Ελληνικά - el
* Русский - ru
* Українська - uk
* 日本語 - ja

And restart your bot
  ```sh
$ systemctl restart ethvaltgbot.service 
```

## What to do if something not working?
Find in bot.py telebot.logger.setLevel(logging.ERROR) and change ERROR to DEBUG, restart tontgbot service and execute
  ```sh
$ journalctl -e -u tontgbot > /opt/tontgbot/servicelog.log
```
