from telegram import Bot
from telegram.ext import Updater,CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
import requests
import re
import database as db
import bot_texts
import json

from flask import jsonify



TOKEN = '949953945:AAHTXEKVQfgI7zxjZQeFcTxNT0SalBtGFjk'
city_num = [str(i) for i in range(1, 4)]


def parse_message(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    username = message['message']['chat']['username']
    message_id = message['message']['message_id']

    pattern = r'/[a-zA-Z]{2,}'
    ticker = re.findall(pattern, text)
    content = ""
    if ticker:
        content = ticker[0][1:]
        type = 1
    else:
        content = text
        type = 2

    return int(chat_id), type, content, username, int(message_id)

def proces_contact(message):
    user_id = int(message['message']['chat']['id'])
    phone_number = message['message']['contact']['phone_number']
    if "first_name" in message['message']['from'].keys():
        firstname = message['message']['from']['first_name']
    else:
        firstname = None

    if "last_name" in message['message']['from'].keys():
        lastname = message['message']['from']['last_name']
    else:
        lastname = None

    if "username" in message['message']['from'].keys():
        username = message['message']['from']['username']
    else:
        username = None

    out_tuple = (user_id, phone_number, firstname, lastname, username)
    return out_tuple


def parse_image_message(msg):
    user_id = msg['message']['chat']['id']
    file_id = msg['message']['photo'][0]['file_id']
    message_id = msg['message']['message_id']
  
    if 'caption' in msg['message'].keys():
        caption = msg['message']['caption']
    else:
        caption = None

    return user_id, message_id, file_id, caption


def parse_video_message(msg):
    user_id = msg['message']['chat']['id']
    file_id = msg['message']['video']['file_id']
    message_id = msg['message']['message_id']
  
    if 'caption' in msg['message'].keys():
        caption = msg['message']['caption']
    else:
        caption = None

    return user_id, message_id, file_id, caption



def regularTextHandler(user_id, content, message_id, type=1):
    aliases = db.get_aliases(user_id)
    if content == '📝 ارسال گزارش':
        return select_reporting(user_id)

    elif content == '😉 سبزی پاک کنیم':
        return select_CleaningVegetable(user_id)

    elif content == '❓ قوانین و راهنما':
        return help(user_id)

    elif content == '👤 پروفایل':
        return select_profile(user_id)

    elif content == 'انتخاب نام مستعار':
        aliases = db.get_aliases(user_id)
        if len(aliases) == 0:
            return get_alias_from_user_while_reporting(user_id)
        else:
            return choose_aliases(user_id, aliases)
    elif content == '💰 امتیازات':
        return show_scores(user_id)
    elif content == '❌ تمایلی ندارم':
        return restart(user_id)
    elif content == 'شروع مجدد':
        return start(user_id)
    elif content == "\U000027A1 بازگشت به منو اصلی":
        return menu(user_id)
    elif content == "\U000021AA بازگشت به پروفایل":
        return select_profile(user_id)
    elif content in city_num:
        return get_report(user_id, content)
    elif content == '\U00002712 نوشتن گزارش':
        return start_reporting(user_id)
    elif content == '\U0001F465 افزودن نام مستعار جدید':
        return add_new_alias_profile(user_id)
    elif content in aliases:
        return select_city(user_id, content)
    else:
        cState, = db.get_state(user_id)[0]
        if cState == 12:
            return regester_new_alias(user_id, content)
        elif cState == 14:
            return report_sent(user_id, content, message_id, type=1)
        elif cState == 22:
            reply_markup = {'keyboard': [[{'text':'\U000021AA بازگشت به پروفایل'}],[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
            state22_text = "نام مستعار شما با موقییت اضافه شد"
            send_message(chat_id=user_id, text=state22_text, reply_markup=reply_markup)
            num = len(aliases) + 1
            db.add_alias(user_id, content, num)
            return 23

# New change. make sure there is no rideman in performance
        else:
            return cState
        

def photoMessageHandler(user_id, file_id, caption, message_id):
    print("\n\n\n photo message handler \n\n\n")
    cState = db.get_state(user_id)
    cState, = cState[0]
    print("\n\n cState = {}\n\n".format(cState))
    if cState == 14:
        print(" \n\n\n return_state = report_sent\n\n\n")
        return report_sent(user_id=user_id, text=caption, message_id=message_id, type=2,file_id=file_id) 
    print(" \n\n\n return_state = cState\n\n\n")
    return cState


def videoMessageHandler(user_id, file_id, caption, message_id):
    print("\n\n\n photo message handler \n\n\n")
    cState = db.get_state(user_id)
    cState, = cState[0]
    print("\n\n cState = {}\n\n".format(cState))
    if cState == 14:
        print(" \n\n\n return_state = report_sent\n\n\n")
        return report_sent(user_id=user_id, text=caption, message_id=message_id, type=3 ,file_id=file_id) 
    print(" \n\n\n return_state = cState\n\n\n")
    return cState


def commandHandler(chat_id, content):
    print("\n********** command handler **********")
    if content == 'start':
        response = start(chat_id)
        return response
    elif content == 'help':
        response = help(chat_id)
        return response



def send_message(chat_id, text, reply_markup=None, parse_mode=None, reply_to_message_id=None):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    if reply_markup is not None:
        payload['reply_markup'] = reply_markup

    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id


    r = requests.post(url, json=payload)
    # r = requests.post(url)
    return r


def send_photo(user_id, file_id, caption, reply_markup=None, parse_mode=None, reply_to_message_id=None):
    bot = Bot(token=TOKEN)
    bot.send_photo(chat_id=user_id, photo=file_id, caption=caption, reply_markup=reply_markup, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode)


def send_video(user_id, file_id, caption, reply_markup=None, parse_mode=None, reply_to_message_id=None):
    bot = Bot(token=TOKEN)
    bot.send_video(chat_id=user_id, video=file_id, caption=caption, reply_markup=reply_markup, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode)


def start(chat_id):
    print(" **********  start ***********")
    search_userId_result = db.search_userId(chat_id)
    if search_userId_result == 1:
        db.drop_cache(chat_id)
        response = menu(chat_id) 
        return response
    elif search_userId_result == -1: 
        response = register_new_user(chat_id)
        return response


def register_new_user(user_id):
    reply_markup = {'keyboard': [[{'text': '\U00002705 ارسال شماره تماس', 'request_contact': True}], [{'text': '\U0000274C تمایلی ندارم'}]], 'resize_keyboard': True, 'one_time_keyboard': True}
    reply_markup = json.dumps(reply_markup)
    get_contact_text = bot_texts.get_getContactText()
    send_message(chat_id=user_id, text=get_contact_text, reply_markup=reply_markup)
    return 1


def menu(chat_id):
    reply_markup = {"keyboard": [[{"text":"\U0001F609 سبزی پاک کنیم "}, {'text': '\U0001F4DD ارسال گزارش'}], [{"text":"\U0001F464 پروفایل"}, {'text': '\U00002753 قوانین و راهنما'}]], 
        "resize_keyboard": True, "one_time_keyboard": True }

    start_text =  bot_texts.get_startText()
    send_message(chat_id=chat_id, text=start_text, reply_markup=reply_markup)
    return 3



def help(chat_id):
    help_text = bot_texts.get_helpText()
    reply_markup = {'keyboard': [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], 'resize_keyboard': True, 'one_time_keyboard': True}
    send_message(chat_id, help_text, parse_mode='Markdown', reply_markup=reply_markup)
    return 15



def select_city(chat_id, selected_alias):
    db.cache_alias(chat_id, selected_alias)
    reply_markup = {'keyboard': [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], 'resize_keyboard': True, 'one_time_keyboard': True}
    send_message(chat_id, text=bot_texts.selected_alias_goto_city(), reply_markup=reply_markup)
    return 13


def select_profile(chat_id):
    reply_markup = {"keyboard": [[{"text": '\U0001F4B0 امتیازات'}, {"text":'\U0001F465 افزودن نام مستعار جدید'}], [{'text': '\U000027A1 بازگشت به منو اصلی'}]], 
        "resize_keyboard": True, "one_time_keyboard": True }

    start_text =  bot_texts.get_profileSetting_text()
    send_message(chat_id=chat_id, text=start_text, reply_markup=reply_markup, parse_mode="Markdown")
    return 4


def show_scores(chat_id):
    t = db.get_coins(chat_id)
    coin, cash = t[0]
    # coin, cash = database.get_coins(chat_id)
    reply_markup = {'keyboard': [[{'text':'\U000021AA بازگشت به پروفایل'}],[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    text = f'\U0001F4B0 سکه : {coin}\n \U0001F4B3 اعتبار : {cash}\n.'
    send_message(chat_id, text=text, reply_markup=reply_markup)
    return 5
                                        

def choose_aliases(chat_id, aliases):
    text = bot_texts.get_getAliasesText()
    reply_markup = {}

    if len(aliases) == 1:
        reply_markup = {"keyboard": [[{'text': aliases[0]}]], "resize_keyboard": True, "one_time_keyboard": True }
    elif len(aliases) == 2:
        reply_markup = {"keyboard": [[{'text': aliases[0]}, {'text' : aliases[1]}]], "resize_keyboard": True, "one_time_keyboard": True }
    else:
        reply_markup = {"keyboard": [[{'text': aliases[0]}, {'text': aliases[1]}, {'text': aliases[2]}]], "resize_keyboard": True, "one_time_keyboard": True }

    send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    return 11


# TODO: is_reporting must became False after reporting finished (Done button / Cancel button)

def select_reporting(chat_id):
    # is_reporting = True
    db.drop_cache(chat_id)
    describe_text = bot_texts.get_describeText()
    reply_markup = {"keyboard": [[{'text':"انتخاب نام مستعار"}], [{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True }
    send_message(chat_id=chat_id, text=describe_text, reply_markup=reply_markup)
    return 10


def get_alias(user_id):
    text = bot_texts.get_enterNewAliasText()
    reply_markup = {"keyboard": [[{'text': "بازگشت به منو اصلی"}, {'text': 'بازگشت به پروفایل'}]], "resize_keyboard": True, "one_time_keyboard": True }
    send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    return 7


def restart(user_id):
    reply_markup = {'keyboard' : [[{'text' : 'شروع مجدد'}]], "resize_keyboard": True, "one_time_keyboard": True}
    text = bot_texts.get_denyText()
    send_message(text=text, chat_id=user_id, reply_markup=reply_markup)
    return 2


def get_alias_from_user_while_reporting(user_id):
    reply_markup = {'keyboard': [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    text = bot_texts.getAliases_while_reporting_text()
    send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    return 12


def select_CleaningVegetable(user_id):
    reply_markup = {'keyboard': [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    send_message(chat_id=user_id, text=bot_texts.get_vegCleaningText(), reply_markup=reply_markup)
    return 17


def regester_new_alias(user_id, alias):
    print("\n\n\n regester new alias \n\n\n")
    db.add_alias(user_id, alias, 1)
    db.cache_alias(user_id, alias)
    reply_markup = {"keyboard": [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    send_message(chat_id=user_id, text=bot_texts.selected_alias_goto_city(), reply_markup=reply_markup)
    return 13



def report_sent(user_id, text, message_id, type, file_id=None):
    print("\n\n\n report sent\n\n\n")
    city, alias = db.insert_report(user_id, text, message_id, file_id)  
    print(f"\n\n\nfile_id = {file_id}\ncity = {city}\nalias = {alias}\n\n\n")
    if city is not None and alias is not None:
        reply_markup = {"keyboard": [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
        send_message(chat_id=user_id, text=bot_texts.report_succ_sent, reply_markup=reply_markup)
        db.empty_cache(user_id)
        send_to_admin(text, city, alias, type, file_id)
        # db.add_to_waiting_reports(user_id, text)
        db.drop_cache(user_id)
    return 19


def get_report(user_id, content):
    db.cache_city(user_id, int(content))
    reply_markup = {'keyboard': [[{'text': '\U00002712 نوشتن گزارش'}], [{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    send_message(chat_id=user_id, text=bot_texts.city_selected_goto_report(), reply_markup=reply_markup)
    return 18


def start_reporting(user_id):
    reply_markup = {'keyboard': [[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
    send_message(chat_id=user_id, text=bot_texts.send_report(), reply_markup=reply_markup)
    return 14


def add_new_alias_profile(user_id):
    aliases = db.get_aliases(user_id)

    if len(aliases) == 3:
        reply_markup = {'keyboard': [[{'text':'\U000021AA بازگشت به پروفایل'}],[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
        text = """\U00002639
        شما تعداد 3 نام مستعار مجاز خودتان را ثبت کرده اید"""
        send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
        return 21
    else:
        reply_markup = {'keyboard': [[{'text':'\U000021AA بازگشت به پروفایل'}],[{'text': '\U000027A1 بازگشت به منو اصلی'}]], "resize_keyboard": True, "one_time_keyboard": True}
        text = bot_texts.get_add_new_alias()
        send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
        return 22

def city_text(city_number):
    city_num = int(city_number)
    if city_num == 1:
        return 'مشهد'
    elif city_num == 2:
        return "تهران"
    elif city_num == 3:
        return "اصفهان"



def send_to_admin(text, city, alias, type, file_id=None):
    print("\n\n\n send to admin started \n\n\n")
    admins = get_admins()
    for admin in admins:
        user_id = admin
        city = city_text(city)
        print(f"\n\n\ncity = {city}\nalias = {alias}\nfile_id = {file_id}\n\n\n")
        report_text = text + '\n __________________' + "\n\n" + "|" + alias + "|" + "\n شهر محل گزارش: " + city + '\n\n' +'@Mashhadchekhabaar'
        print(f'\n\n\n {admin}')
        reply_markup = {
            'inline_keyboard': [
                # [{'text': '\U00002705 قبول کردن', 'url': accept_url}], 
                [{'text': '\U00002705 قبول کردن', 'callback_data': '1'}], 
                [{'text': '\U0000274C رد کردن', 'callback_data': '2'}]
                ]
        }
        if type == 1:
            send_message(chat_id=user_id, text=report_text, reply_markup=reply_markup)              
        elif type == 2:
            send_photo(user_id=user_id, file_id=file_id, caption=report_text, reply_markup=reply_markup)
        elif type == 3:
            send_video(user_id=user_id, file_id=file_id, caption=report_text, reply_markup=reply_markup)


def get_admins():
    with open('/var/www/html/chekhabar-bot/src/admins.txt', 'r') as file:
        usernames = file.readlines()
    list = []
    for admin in usernames:
        admin = int(admin.strip())
        list.append(admin)
    
    return list


def tell_user_for_acc(report_text):
    user_id, message_id = db.get_report_message_id(report_text)
    text = bot_texts.tell_user_for_acc
    send_message(chat_id=user_id, text=text, reply_to_message_id=message_id)


def tell_user_for_reject(report_text):
    print("\n\n\n tell user for reject\nreport_text = {}\n".format(report_text))
    user_id, message_id = db.get_report_userid_message_id_for_reject(report_text)
    print("user_id = {}\nmessage_id = {}\n".format(user_id, message_id))
    if user_id and message_id:
        text = bot_texts.tell_user_for_reject
        send_message(chat_id=user_id, text=text, reply_to_message_id=message_id)
        print("\nrejection sent to user \n\n\n")

