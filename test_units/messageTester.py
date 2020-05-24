from telebot.Generic import Object


class MessageClass(Object):
    def __init__(self, message_id: int, text: str, chat_id: int, chat_first_name: str, chat_last_name: str):
        self.message_id = message_id
        self.text = text
        self.chat = Object
        self.chat.id = chat_id
        self.chat.first_name = chat_first_name
        self.chat.last_name = chat_last_name


def getMessageSequence(index: int):
    return message_sequences[index % len(message_sequences)]
    pass


NamesTemplates = ['ido', 'nadav', 'gal', 'ben', 'alon', 'adi', 'omer', 'inbal', 'shir', 'dor']

message_sequences = [
    {'texts': ['q1', 'cookie'],
     'responses': ['what is your nickname?', 'now your nickname will be cookie']
     },
    {'texts': ['okay', 'ok', 'OK', 'Ok'],
     'responses': ['OK', 'OK', 'OK', 'OK']
     },
]
