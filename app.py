import re
from time import sleep

from flask import Flask, request, send_file

import telegram
from telegram.botcommand import BotCommand

from telebot.credentials import bot_token, bot_user_name, URL
from telebot.Chat import *

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


# to see logs in REAL TIME login through Heroku CLI(CMD) and write the following line
# heroku logs -a start-telegram-bot --tail


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    print('!!!!!!!!!!!!! message format - VVVVV') # for checking what update returns
    print(update)
    print('')

    if update.callback_query:  # button menu pressed
        data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id
        msg_id = update.callback_query.message.message_id
        print("user pressed on button and returns '%s'" % str(data))
        return 'ok'

    if update.edited_message:
        return 'ok'

    if update.message and update.message.document:
        return 'ok'

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)

    if text == 'showBodyOnServer()':
        print(str(request.data))

    con = Conversation(bot, update.message.chat.id, user=update.message.chat)
    con.MessageAct(bot, message=update.message)

    print("update message is = {}".format(update.message))
    Chat(update.message)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_ok = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # sends telegram a list of optional slashed commands
    commands = [BotCommand('/start', 'starts the process'),
                BotCommand('/help', 'shows the possible actions')]
    commands_ok = bot.set_my_commands(commands=commands)

    return "webhook setup - {webhook} , commands setup - {commands}".format(
        webhook='ok' if webhook_ok else 'failed',
        commands='ok' if commands_ok else 'failed'
    )


@app.route('/')
def index():
    return '.1'


@app.route('/bye_bye')
def other():
    return send_file('animations/bye_bye.mp4')


if __name__ == '__main__':
    app.run(threaded=True)
