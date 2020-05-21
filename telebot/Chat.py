import telegram
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.chataction import ChatAction

from telebot.credentials import bot_user_name, URL

from time import sleep


class Chat:
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.user_id = getattr(message, 'from').id
        print("user_id = {}".format(self.user_id))


class Conversation:
    def __init__(self, bot, chat_id=[], user=[]):
        self.bot = bot
        self.chat_id = chat_id
        self.user = user  # contains id , first_name , is_bot , last_name , language_code
        pass

    def __getitem__(self, item):
        return getattr(self, item)

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
                if "{ReplyMarkup:" in response:
                    string_values = getFormatValues(response, 'ReplyMarkup')
                    options = convertStringToSquaredList(string_values)
                    markup = Response.makeReplyMarkup(options)
                    response = removeFormatName(response, "ReplyMarkup")
                    pass
                if "{InlineMarkup:" in response:
                    string_values = getFormatValues(response, 'InlineMarkup')
                    options = convertStringToSquaredList(string_values)
                    options = [[InlineKeyboardButton(item, callback_data=item) for item in row] for row in options]
                    markup = Response.makeInlineMarkup(options)
                    response = removeFormatName(response, "InlineMarkup")
                    pass
                response = response.format(user=self.user, bot_user_name=bot_user_name)
                return Response.SendText(bot, message, response, markup=markup)

        url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
        Response.SendPhoto(bot, message, url)

        pass  # Act


class Response:

    @staticmethod
    def SendAnimation(bot, message, url, markup=None):
        if markup is None:
            markup = telegram.ReplyKeyboardRemove()
        return bot.send_animation(chat_id=message.chat.id, animation=url,
                                  reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def SendPhoto(bot, message, url):
        bot.sendPhoto(chat_id=message.chat.id, photo=url, reply_to_message_id=message.message_id)

    @staticmethod
    def SendText(bot, message, send_text, markup=None):
        if markup is None:
            markup = telegram.ReplyKeyboardRemove()
        return bot.sendMessage(chat_id=message.chat.id, text=send_text,
                               reply_to_message_id=message.message_id, reply_markup=markup)

    @staticmethod
    def SendTyping(bot, message):
        bot.sendChatAction(chat_id=message.chat.id, action=ChatAction.TYPING)

    @staticmethod
    def makeReplyMarkup(options):
        return ReplyKeyboardMarkup(options)

    @staticmethod
    def makeInlineMarkup(options):
        return InlineKeyboardMarkup(options)


fast_text_responses = [{
    'triggers': ['hi', 'hello', 'hi2'],
    'response': 'hello to you too :)'
}, {
    'triggers': ['/start'],
    'response':  """
            Welcome to coolAvatar bot, 
            the bot is using the service from http://avatars.adorable.io/ 
            to generate cool looking avatars based on the name you enter 
            so please enter a name and the bot will reply with an avatar for your name.
        """
}, {
    'triggers': ['ok', 'okay', 'ko'],
    'response':  'OK'
},
]

fast_animation_responses = [{
    'triggers': ['bye bye', 'bye', 'goodbye'],
    'response': '{}bye_bye'.format(URL),
},
]

user_specific_acts = [{
    'triggers': ['whats my name?', 'what is my name?'],
    'response': "{user.first_name}"
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
    'triggers': ['i got options', 'options', 'option', 'what?', 'help', '/help'],
    'response': "options{ReplyMarkup:'hi','hello':'bye bye','whats your name?':"
                "'whats my full name?','ok':'inline options','/start'}"
}, {
    'triggers': ['inline options'],
    'response': "my options{InlineMarkup:'hi','hello':'bye bye','whats your name?':'whats my full name?'}"
},
]


def removeFormatName(text, format_name):
    remove_from_index = text.find('{' + format_name + ':')
    return text[:remove_from_index] + text[text.find('}', remove_from_index) + 1:]


def getFormatValues(text, format_name):
    start_index = text.find(':', text.find('{' + format_name + ':'))
    end_index = text.find('}', start_index)
    return text[start_index:end_index]


# format of this function is "'1','2':'3','4'" to [['1','2']['3','4']]
def convertStringToSquaredList(text):
    return [(eval("[" + row + "]")) for row in text.split(":")]
