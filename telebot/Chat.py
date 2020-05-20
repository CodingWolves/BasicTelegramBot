import telegram
from telegram.botcommand import BotCommand
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.chataction import ChatAction

from telebot.credentials import bot_token, bot_user_name, URL


class Conversation:
    def __init__(self, bot=telegram.Bot, chat_id=[], user=[]):
        self.bot = bot
        self.chat_id = chat_id
        self.user = user  # contains id , first_name , is_bot , last_name , language_code
        pass

    def __getitem__(self, item):
        if item == 'bot':
            return self.bot
        if item == 'chat_id':
            return self.chat_id
        if item == 'user':
            return self.user

    def Act(self, bot, message):
        text = message.text.encode('utf-8').decode()

        if text in fast_text_responses:
            Response.SendText(bot, message, fast_text_responses[text])

        if text in fast_animation_responses:
            Response.SendAnimation(bot, message, fast_animation_responses[text])

        if text in user_specific_text_responses:
            text = user_specific_text_responses[text]
            if "{KeyboardMarkup:" in text:
                mark_text = text.split("{KeyboardMarkup:")[1]
                mark_text = mark_text.split('}')[0]
                options = [(eval("[" + row + "]")) for row in mark_text.split(":")]  # orders the options
                pass
            text = text.format(user=self.user, bot_user_name=bot_user_name, options=options, KeyboardMarkup=None)
            Response.SendText(bot, message, text)

        pass


class Response:
    remove_reply_markup = telegram.ReplyKeyboardRemove()

    @staticmethod
    def SendAnimation(bot, message, url, markup=remove_reply_markup):
        bot.send_animation(chat_id=message.chat.id, animation=url,
                           reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def SendText(bot, message, send_text, markup=remove_reply_markup):
        bot.sendMessage(chat_id=message.chat.id, text=send_text,
                        reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def getKeyboardMarkup(options=[[]]):
        return ReplyKeyboardMarkup(options)


fast_text_responses = {
    'hi2': 'hello to you too :)',
}

fast_animation_responses = {
    'bye bye': '{}bye_bye'.format(URL),
}

user_specific_text_responses = {
    'whats my name?': "{user.first_name}{KeyboardMarkup:'hi2','bye':'bye'}",
    'what is my name?': '{user.first_name}',
    'whats my family name?': '{user.last_name}',
    'whats my full name?': '{user.first_name} {user.last_name}',
    'whats your name?': 'my name is {bot_user_name}'
}
