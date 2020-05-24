from test_units.messageTester import MessageClass, getCustomizedSequence, getSequenceFromActDict, \
    getRandomSequenceFromActDict
from telebot.Chat import Chat
from telebot.Act import InitializeActs
from telebot.credentials import URL
from random import randint
import random
import datetime

global actions
actions = []

textTemplates = ['bot', 'ok', 'hi', '/start', 'help', 'q1']


def getRandText():
    return textTemplates[randint(0, len(textTemplates) - 1)]


def StartTester():
    smart_seq_total_time = datetime.timedelta()
    garbage_total_time = datetime.timedelta()
    custom_seq_total_time = datetime.timedelta()

    print(random.random())
    global actions
    InitializeActs()

    chats_count = 1000
    garbage_count = 100
    customized_sequences_count = 100
    smart_sequences_count = 100

    bot = BotClass()
    first_messages = [MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                   chat_id=randint(10000, 99999), chat_first_name='ido', chat_last_name='zany')
                      for i in range(chats_count)]
    chats = [Chat(msg) for msg in first_messages]
    for chat in chats:
        assert issubclass(type(chat), Chat)

        msg_time = datetime.datetime.now()
        GarbageSender(bot, chat, garbage_count)
        garbage_total_time += datetime.datetime.now() - msg_time

        GarbageSender(bot, chat, 10, text="abiding")  # resets the chat follow_up because of previous garbage

        custom_seq_time = datetime.datetime.now()
        for _ in range(customized_sequences_count):
            actions.clear()
            sequence = getCustomizedSequence(randint(0, 10000))
            print('new customized sequence - {}'.format(sequence))
            SequenceSender(bot, chat, sequence)
        custom_seq_total_time += datetime.datetime.now() - custom_seq_time

        seq_time = datetime.datetime.now()
        for _ in range(smart_sequences_count):
            sequence = getRandomSequenceFromActDict(chat.data)
            SequenceSender(bot, chat, sequence)
        smart_seq_total_time += datetime.datetime.now() - seq_time

    print('chats count {}'.format(chats_count))
    print('garbage msg count {} , time {}'.format(garbage_count, garbage_total_time))
    print('custom seq count {} , time {}'.format(customized_sequences_count, custom_seq_total_time))
    print('smart seq count {} , time {}'.format(smart_sequences_count, smart_seq_total_time))


def GarbageSender(bot, chat, count: int, text=None):
    messages = None
    if text:
        messages = [MessageClass(message_id=randint(10000, 99999), text=text,
                                 chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                    for i in range(count)]
    else:
        messages = [MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                 chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                    for i in range(count)]
    for msg in messages:
        actions.clear()
        chat.GotMessage(bot=bot, message=msg)
        for action in actions:
            print('action by server - {}'.format(action))


def SequenceSender(bot, chat, sequence):
    global actions
    print('new random sequence formed - {}'.format(sequence))
    actions.clear()
    for text in sequence['texts']:
        print(chat.data.user.first_name)
        chat.GotMessage(bot=bot, message=MessageClass(message_id=randint(10000, 99999), text=text,
                                                      chat_id=chat.id, chat_first_name='ido',
                                                      chat_last_name='zany'))
    CheckResponseActions(sequence)


def CheckResponseActions(sequence):
    for i in range(len(sequence['responses'])):
        response = sequence['responses'][i]
        if len(actions) > i:
            if 'text' in actions[i] and actions[i]['text'] == response:
                print('checked action for server - {}'.format(actions[i]))
            elif 'animation' in actions[i] and actions[i]['animation'] == response:
                print('checked action for server - {}'.format(actions[i]))
            else:
                print(actions)
                raise Exception("response was not correct '{}' , needed '{}'".format(actions[i], response))
        else:
            raise Exception('fewer actions by server than expected'.format())
    if len(actions) > len(sequence['responses']):
        print('Unexpected Actions ---')
        for i in range(len(sequence['responses']), len(actions), 1):
            print('action by server - {}'.format(actions[i]))
        raise Exception("more responses than expected".format())


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
