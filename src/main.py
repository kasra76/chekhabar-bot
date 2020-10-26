import json
import re
import requests
import database as db
import bot_functions 
import bot_texts
import semaphore
from flask import Flask, request, Response
from threading import Thread
from admin_server import AdminMessage
from inlineKeyboardHandler import InLineKeyboardHandler
from telegram import Bot

app = Flask(__name__)
TOKEN = bot_functions.TOKEN
URL = "https://chekhabar.ratintech.com"
Semaphore = semaphore.Semaphore()
bot = Bot(token=TOKEN)


@app.route('/', methods=['POST'])
def index():

    # contains json object that telegram sent
    msg = request.get_json()
    with open('request.json', 'w', encoding='utf-8') as file:
        json.dump(msg, file, ensure_ascii=False, indent=4)  

    # admins = bot_functions.get_admins()
    admins = bot_functions.get_admins()

    if 'message' in msg.keys():
        if 'contact' in msg['message'].keys():
            user_id, phone_number, firstname, lastname, username = bot_functions.proces_contact(msg)
            state = db.get_state(user_id)
            response_state = db.add_user(user_id=user_id, phone_number=phone_number, firstname=firstname, lastname=lastname, username=username)
            db.update_state(user_id=user_id, state=int(response_state))
            bot_functions.menu(user_id)
        elif 'photo' in msg['message'].keys():
            user_id, message_id, file_id, caption = bot_functions.parse_image_message(msg)
            state = db.get_state(user_id)
            if len(state) == 0:
                print("\n\n not enter in key part \n\n")
                state = 0
            else:
                print("\n\n enter in key part \n\n")
                state, = state[0]
            
            ligal = Semaphore.is_ligal(caption, user_id, state)
            if ligal:
                returned_state = bot_functions.photoMessageHandler(user_id, file_id, caption, message_id)
                db.update_state(user_id, returned_state)
            else:
                bot_functions.send_message(chat_id=user_id, text=bot_texts.get_illigalText())

        elif 'video' in msg['message'].keys():
            user_id, message_id, file_id, caption = bot_functions.parse_video_message(msg)
            state = db.get_state(user_id)
            if len(state) == 0:
                print("\n\n not enter in key part \n\n")
                state = 0
            else:
                print("\n\n enter in key part \n\n")
                state, = state[0]
            
            ligal = Semaphore.is_ligal(caption, user_id, state)
            if ligal:
                returned_state = bot_functions.videoMessageHandler(user_id, file_id, caption, message_id)
                db.update_state(user_id, returned_state)
            else:
                bot_functions.send_message(chat_id=user_id, text=bot_texts.get_illigalText())
            
        else:
            # parsing the message
            user_id, type, content, username, message_id = bot_functions.parse_message(msg)
            state = db.get_state(user_id)  
            if user_id in admins:
                admin_mesage = AdminMessage(user_id)
                if type == 1:
                    returned_state = admin_mesage.commandHandler(content)
            else:
                if len(state) == 0:
                    print("\n\n\n state = 0\n\n\n")
                    state = 0
                else:
                    state, = state[0]
                print(" \n\n type = ", state, " \n\n")
                # bot_functions.send_message(chat_id=chat_id, text=state)    
                ligal = Semaphore.is_ligal(content, user_id, state)
                if ligal:
                    if type == 1:
                        returned_state = bot_functions.commandHandler(user_id, content)
                        db.update_state(user_id, returned_state)
                        print("\n\n\n state updated : {} \n\n\n".format(returned_state))
                    else:
                        returned_state = bot_functions.regularTextHandler(user_id, content, message_id)
                        db.update_state(user_id, returned_state)
                else:
                    bot_functions.send_message(chat_id=user_id, text=bot_texts.get_illigalText())
    elif 'callback_query' in msg.keys():
        handler = InLineKeyboardHandler(msg)
        handler.execute()
    return Response('ok', status=200)

@app.route('/', methods=['GET'])
def indexx():
    return Response('OK', status=200)


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')
