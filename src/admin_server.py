from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, CallbackQuery
from telegram.ext import Updater,CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
import requests
import re
import database, admin_database
import admin_text
import json
import bot_functions
import semaphore
import json
from telegram import Bot

CHANNEL_ID = '@chkhtest'
TOKEN = '949953945:AAHTXEKVQfgI7zxjZQeFcTxNT0SalBtGFjk'



class AdminMessage:
    def __init__(self, user_id):
        self.user_id = user_id

    
    def send_message_to_channel(self, text, type, file_id=None, reply_markup=None, parse_mode=None):
        print("\n\n\n comes in send to channel method \n\n\n")
        if type == 1:
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            payload = {'chat_id': CHANNEL_ID, 'text': text, 'video': file_id}

        elif type == 2:  
            url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
            payload = {'chat_id': CHANNEL_ID, 'caption': text, 'photo': file_id}

        elif type == 3:
            url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
            payload = {'chat_id': CHANNEL_ID, 'caption': text, 'video': file_id}


        if reply_markup is not None:
                payload['reply_markup'] = reply_markup

        if parse_mode is not None:
            payload['parse_mode'] = parse_mode


        r = requests.post(url, json=payload)
        # print(f"\n\n\n request = {r.body.message} \n\n\n")
        with open('send_to_channel_msg.json', 'w', encoding='utf-8') as file:
            json.dump(r.json(), file, ensure_ascii=False, indent=4) 
        # r = requests.post(url)
        return r.json()


    def commandHandler(self, content):
        if content == "start":
            return self.admin_start()

    

    def admin_start(self):
        text = admin_text.start_text
        bot_functions.send_message(chat_id=self.user_id, text=text)
        return 101
