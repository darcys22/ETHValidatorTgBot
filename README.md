# EthValTgBot Readme
This is telegram bot for your Validator. 

This bot can only send messages to your telegram id

## Installation in 5 simple steps (2-3 minutes, and your bot is ready)

 1. Create your personal telegram bot and get Api Token. [Instruction](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0)
 2. Send to your new bot command /start and go to the next step
 3. Run command below
```sh
$ cd $HOME && git clone -v https://github.com/darcys22/EthValTgBot.git ethvaltgbot && cd ./ethvaltgbot && chmod +x ./installsbot.sh
```
 4. Create ./config.py using the template example-config.py in any editor and change values from *Edit starts here* till *Edit ends here*. If you dont know your id(tg value), Just send message to @TONTgIDBot in telegram. Then open ./sbot.sh and put user folder at lines 14-15. Open ./ethvaltgbot.service and put user&group at lines 7-8
 
 5. Run 
 ```sh
$ /bin/bash ./installsbot.sh
```

## Available languages *Yes, with google translate
Change languages=['en'] in bot.py to language, what you need
  ```sh
lang_translations = gettext.translation('base', localedir='/opt/ethvaltgbot/locales', languages=['en'])
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
Find in bot.py telebot.logger.setLevel(logging.ERROR) and change ERROR to DEBUG, restart ethvaltgbot service and execute
  ```sh
$ journalctl -e -u ethvaltgbot > /opt/ethvaltgbot/servicelog.log
```
