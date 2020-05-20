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

    def MessageAct(self, bot, message):
        text = message.text.encode('utf-8').decode()
        markup = None

        for response in fast_text_responses:
            if text in response.triggers:
                return Response.SendText(bot, message, response.response)

        if text in fast_animation_responses:
            return Response.SendAnimation(bot, message, fast_animation_responses[text])

        if text in user_specific_text_responses:
            text = user_specific_text_responses[text]
            if "{KeyboardMarkup:" in text:
                mark_text = text.split("{KeyboardMarkup:")[1]
                mark_text = mark_text.split('}')[0]
                options = [(eval("[" + row + "]")) for row in mark_text.split(":")]  # orders the options
                markup = Response.makeKeyboardMarkup(options)
                text = text[:text.rfind('{')]
                pass
            text = text.format(user=self.user, bot_user_name=bot_user_name)
            return Response.SendText(bot, message, text, markup=markup)

        pass


class Response:
    remove_reply_markup = telegram.ReplyKeyboardRemove()

    @staticmethod
    def SendAnimation(bot, message, url, markup=remove_reply_markup):
        return bot.send_animation(chat_id=message.chat.id, animation=url,
                                  reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def SendText(bot, message, send_text, markup=remove_reply_markup):
        return bot.sendMessage(chat_id=message.chat.id, text=send_text,
                               reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def makeKeyboardMarkup(options):
        return ReplyKeyboardMarkup(options)


fast_text_responses = [{
    'triggers': ['hi', 'hello', 'hi2'],
    'response': 'hello to you too :)'
}]

fast_animation_responses = {
    'bye bye': '{}bye_bye'.format(URL),
}

user_specific_text_responses = {
    'whats my name?': "{user.first_name}{KeyboardMarkup:'hi2','bye':'bye bye'}",
    'what is my name?': '{user.first_name}',
    'whats my family name?': '{user.last_name}',
    'whats my full name?': '{user.first_name} {user.last_name}',
    'whats your name?': 'my name is {bot_user_name}'
}
