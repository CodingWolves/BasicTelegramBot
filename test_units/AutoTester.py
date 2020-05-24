from test_units.messageTester import MessageClass, getMessageSequence
from telebot.Chat import Chat
from telebot.Act import InitializeActs
from random import randint
import random

global actions
actions = []

textTemplates = ['bot', 'ok', 'hi', '/start', 'help', 'q1']


def getRandText():
    return textTemplates[randint(0, len(textTemplates) - 1)]


def StartTester():
    print(random.random())
    global actions
    InitializeActs()
    chats_count = 1000
    messages_count = 100
    bot = BotClass()
    first_messages = [MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                   chat_id=randint(10000, 99999), chat_first_name='ido', chat_last_name='zany')
                      for i in range(chats_count)]
    chats = [Chat(msg) for msg in first_messages]
    for chat in chats:
        assert issubclass(type(chat), Chat)
        messages = [MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                 chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                    for i in range(messages_count)]

        for msg in messages:
            actions.clear()
            chat.GotMessage(bot=bot, message=msg)
            pass

        for _ in range(6):
            chat.GotMessage(bot=bot, message=MessageClass(message_id=randint(10000, 99999), text='abiding',
                                                          chat_id=chat.id, chat_first_name='ido', chat_last_name='zany'))

        message_sequences = [getMessageSequence(randint(0, 999999)) for _ in range(100)]
        for message_sequence in message_sequences:
            actions.clear()
            for text in message_sequence['texts']:
                chat.GotMessage(bot=bot, message=MessageClass(message_id=randint(10000, 99999), text=text,
                                                              chat_id=chat.id, chat_first_name='ido', chat_last_name='zany'))
            for response in message_sequence['responses']:
                if actions[0]['text'] == response:
                    actions.pop(0)
                else:
                    raise Exception("response was not correct '{}' , needed '{}'".format(actions[0], response))


class BotClass:
    def sendMessage(self, chat_id=0, text='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        global actions
        actions.append({
            'action': 'sendMessage',
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })

    def sendAnimation(self, chat_id=0, animation='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        global actions
        actions.append({
            'action': 'sendAnimation',
            'chat_id': chat_id,
            'animation': animation,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })


StartTester()
