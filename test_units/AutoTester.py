from test_units.messageTester import MessageClass, getMessageSequence
from telebot.Chat import Chat
from telebot.Act import InitializeActs
from random import randint
import random
import datetime

global actions
actions = []

textTemplates = ['bot', 'ok', 'hi', '/start', 'help', 'q1']


def getRandText():
    return textTemplates[randint(0, len(textTemplates) - 1)]


def StartTester():
    seq_total_time = datetime.timedelta()
    msg_total_time = datetime.timedelta()


    print(random.random())
    global actions
    InitializeActs()
    chats_count = 1000
    messages_count = 10
    sequences_count = 10
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

        msg_time = datetime.datetime.now()
        for msg in messages:
            actions.clear()
            chat.GotMessage(bot=bot, message=msg)
            for action in actions:
                print('action by server - {}'.format(action))
            pass
        msg_total_time += datetime.datetime.now() - msg_time

        for _ in range(6):
            chat.GotMessage(bot=bot, message=MessageClass(message_id=randint(10000, 99999), text='abiding',
                                                          chat_id=chat.id, chat_first_name='ido', chat_last_name='zany'))
        seq_time = datetime.datetime.now()
        message_sequences = [getMessageSequence(randint(0, 999999)) for _ in range(sequences_count)]
        for message_sequence in message_sequences:
            actions.clear()
            print('new message sequence started {}'.format(message_sequence))
            for text in message_sequence['texts']:
                chat.GotMessage(bot=bot, message=MessageClass(message_id=randint(10000, 99999), text=text,
                                                              chat_id=chat.id, chat_first_name='ido', chat_last_name='zany'))
            for response in message_sequence['responses']:
                if len(actions) > 0:
                    if actions[0]['text'] == response:
                        print('action by server - {}'.format(actions.pop(0)))
                    else:
                        raise Exception("response was not correct '{}' , needed '{}'".format(actions[0], response))
                else:
                    raise Exception('fewer actions by server than expected'.format())
            if len(actions) > 0:
                print('Unexpected Actions')
                for action in actions:
                    print('action by server - {}'.format(action))
                raise Exception("more responses than expected, ".format(actions[0], response))
        seq_total_time += datetime.datetime.now() - seq_time

    print('msg time {}'.format(msg_total_time))
    print('seq time {}'.format(seq_total_time))


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
