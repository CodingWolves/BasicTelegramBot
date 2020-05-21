import telegram

from telebot.credentials import bot_user_name, URL
from telebot.Act import Act, FollowUp

from time import sleep


class Chat:
    def __init__(self, message):
        self.id = message.chat.id
        self.user = {
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name,
        }
        self.data = {}
        self.follow_up_act = False
        self.unhandled_messages = []

    def GotMessage(self, bot, message):
        text = message.text.encode('utf-8').decode()
        if self.follow_up_act:
            self.follow_up_act = self.follow_up_act.doAct(bot, self, message)
            return
            pass

        act = Act.getActByTrigger(text)
        if act is Act:
            follow_up_act = act.doAct(bot, self, message)
            if follow_up_act:
                self.follow_up_act = follow_up_act

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
