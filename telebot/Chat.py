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
            Response.text(bot, message, fast_text_responses[text])

        if text in fast_animation_responses:
            Response.animation(bot, message, fast_animation_responses[text])

        if text in user_specific_text_responses:
            text = user_specific_text_responses[text]
            text = text.format(user=self.user)


            # segments = user_specific_text_responses[text].split('.')
            # pulled_text = segmentPull(self, segments)
            Response.text(bot, message, text)

        pass


def segmentPull(cls, segments):
    if len(segments) == 1:
        return cls[segments[0]]
    elif len(segments) > 1:
        return segmentPull(cls[segments[0]], segments[1:])


class Response:
    remove_reply_markup = telegram.ReplyKeyboardRemove()

    @staticmethod
    def animation(bot, message, url):
        bot.send_animation(chat_id=message.chat.id, animation=url,
                           reply_to_message_id=message.message_id, reply_markup=Response.remove_reply_markup)

    @staticmethod
    def text(bot, message, send_text):
        bot.sendMessage(chat_id=message.chat.id, text=send_text,
                        reply_to_message_id=message.message_id, reply_markup=Response.remove_reply_markup)


fast_text_responses = {
    'hi2': 'hello to you too :)',
}

fast_animation_responses = {
    'bye2': '{}bye_bye'.format(URL),
}

user_specific_text_responses = {
    'whats my name?': '{user.first_name}',
}
