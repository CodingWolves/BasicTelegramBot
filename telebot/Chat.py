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

        for act in fast_text_responses:
            if text in act['triggers']:
                return Response.SendText(bot, message, act['response'])

        for act in fast_animation_responses:
            if text in act['triggers']:
                return Response.SendAnimation(bot, message, act['response'])

        for act in user_specific_acts:
            if text in act['triggers']:
                response = act['response']
                if "{KeyboardMarkup:" in response:
                    string_values = getFormatValues(response, 'KeyboardMarkup')
                    options = convertStringToSquaredList(string_values)
                    markup = Response.makeKeyboardMarkup(options)
                    response = removeFormatName("KeyboardMarkup")
                    pass
                response = response.format(user=self.user, bot_user_name=bot_user_name)
                return Response.SendText(bot, message, response, markup=markup)

        pass  # Act


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
},
]

fast_animation_responses = [{
    'triggers': ['bye bye', 'bye', 'goodbye'],
    'response': '{}bye_bye'.format(URL),
},
]

user_specific_acts = [{
    'triggers': ['whats my name?', 'what is my name?'],
    'response': "{user.first_name}{KeyboardMarkup:'hi2','bye':'bye bye'}"
}, {
    'triggers': ['what is my full name?', 'whats my full name?'],
    'response': "{user.first_name} {user.last_name}"
}, {
    'triggers': ['what is my family name?', 'whats my family name?'],
    'response': "{user.last_name}"
}, {
    'triggers': ['whats your name?', 'what is your name?', 'what is ur name?', 'whats ur name?'],
    'response': "my name is {bot_user_name}"
}, {
    'triggers': ['i got options'],
    'response': "{KeyboardMarkup:'hi','hello':'bye bye','whats your name?':'whats my full name?'}"
},
]


def removeFormatName(text, format_name):
    remove_from_index = text.find('{' + format_name + ':')
    return text[:remove_from_index] + text[text.find('}', remove_from_index) + 1:]


def getFormatValues(text, format_name):
    start_index = text.find(':', text.find('{' + format_name + ':'))
    end_index = text.find('}', start_index)
    return text[start_index:end_index]


# format of this function is '1','2':'3','4' to [['1','2']['3','4']]
def convertStringToSquaredList(text):
    return [(eval("[" + row + "]")) for row in text.split(":")]
