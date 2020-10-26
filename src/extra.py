from flask import Flask, request
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

global bot
global TOKEN
TOKEN = '949953945:AAFGr3pENyNTepZciXXqCzpjJsvNO-p-iNE'
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


def start(update):
    print('************ start ********************')
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


# @app.route('/{}'.format(TOKEN), methods=['POST'])
@app.route('/', methods=['POST'])
def respond():
    print('respond function has been started')
    # update = telegram.Update.de_json(request.get_json(force=True), bot)
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    # else:
    #     bot.send_message(chat_id=chat_id, text='it is not defined', reply_to_message_id=msg_id)
    updater.idle()
    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    print("set_webhook has been started")
    s = bot.set_webhook('{}{}'.format('https://e7fb28e6.ngrok.io/',TOKEN))
    if s:
        return 'webhook setup ok'
    else:
        return 'webhook setup failed'


@app.route('/')
def index():
    print("index has been started")
    return '.'



if __name__ == '__main__':
    print('main hase been started')
    app.run(threaded=False)



