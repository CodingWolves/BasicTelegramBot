import re
from time import sleep

from flask import Flask, request, send_file

import telegram
from telegram.botcommand import BotCommand
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.chataction import ChatAction

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
        print('user pressed on button and returns %s' % str(data))
        return 'ok'

    if update.edited_message:
        return 'ok'

    if update.message and update.message.document:
        return 'ok'

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)

    if text == 'showBodyOnServer()':
        print(str(request.data))

    if text == "/start":
        bot_welcome = """
            Welcome to coolAvatar bot, 
            the bot is using the service from http://avatars.adorable.io/ 
            to generate cool looking avatars based on the name you enter 
            so please enter a name and the bot will reply with an avatar for your name.
        """
        # shows 'typing...' for 2 seconds
        bot.sendChatAction(chat_id=chat_id, action=ChatAction.TYPING)
        sleep(2)
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
        try:
            # sends buttons on screen below the text sent, when pressed returns the callback_data value
            buttons = [[InlineKeyboardButton('yes', callback_data='y')],
                       [InlineKeyboardButton('no', callback_data='n')]]
            menu_markups = InlineKeyboardMarkup(buttons)
            bot.sendMessage(chat_id=chat_id, message_id=msg_id, text='starting menu', reply_markup=menu_markups)
        except Exception as err:
            print('!!!!!!!!problem with buttons!!!!!!')
            print('buttons error - %s' % str(err))
    elif text == "hi":
        respond_text = "hello to you too :)"
        bot.sendMessage(chat_id=chat_id, text=respond_text, reply_to_message_id=msg_id)
    elif text == "bye":
        # animation needs to be a reachable video url
        bot.send_animation(chat_id=chat_id, animation='{}bye_bye'.format(URL), reply_to_message_id=msg_id)
    elif text == 'help' or text =='/help':
        options = [['hi', 'ok'],
                   ['bye', 'name']]
        reply_markups = ReplyKeyboardMarkup(options)
        bot.sendMessage(chat_id=chat_id, text='those are your options', reply_markup=reply_markups)
    elif text == 'ok':
        remove_reply_markup = telegram.ReplyKeyboardRemove()
        bot.sendMessage(chat_id=chat_id, text='Ok', reply_markup=remove_reply_markup)
    else:
        con = Conversation(bot, chat_id, user=update.message['from'])
        con.Act(bot, message=update.message)
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            print(text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id,
                            text="There was a problem in the name you used, please enter different name",
                            reply_to_message_id=msg_id)

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
