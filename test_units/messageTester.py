from telebot.Generic import Object
from telebot.ActDict import ActionsDictionary, ActType
from random import randint
from telebot.credentials import URL


class MessageClass(Object):
    def __init__(self, message_id: int, text: str, chat_id: int, chat_first_name: str, chat_last_name: str):
        super(MessageClass, self).__init__()
        self.message_id = message_id
        self.text = text
        self.chat = Object
        self.chat.id = chat_id
        self.chat.first_name = chat_first_name
        self.chat.last_name = chat_last_name


def getCustomizedSequence(index: int):
    return message_sequences[index % len(message_sequences)]
    pass


def getRandomSequenceFromActDict(server_data=Object()):
    index = randint(0, len(ActionsDictionary) - 1)
    while len(ActionsDictionary[index]['triggers']) == 0:
        index = randint(0, len(ActionsDictionary) - 1)
    return getSequenceFromActDict(ActionsDictionary[index]['id'], server_data=server_data)


def getSequenceFromActDict(act_id: int, server_data=Object(), is_follow_up=False):
    action_dict = None
    for act in ActionsDictionary:
        if act['id'] == act_id:
            action_dict = act
            break
    if not action_dict:
        raise Exception('cant find id - {}'.format(act_id))
    print('act_id - {} , is_follow_up - {} , data - {}'.format(act_id, is_follow_up, server_data))

    user_messages = []
    server_messages = []
    if not is_follow_up:
        if action_dict['type'] == ActType.Text or action_dict['type'] == ActType.Animation:
            user_msg = None
            if len(action_dict['triggers']) > 0:
                user_msg = action_dict['triggers'][randint(0, len(action_dict['triggers'])-1)]
                user_messages.append(user_msg)
            server_msg = action_dict['data'].format(text_message=user_msg, data=server_data, URL=URL)
            server_messages.append(server_msg)
        elif action_dict['type'] == ActType.SaveCommand:
            data_name = action_dict['save_to_data_name']
            server_data[data_name] = action_dict['data'].format(data=server_data)
        else:
            raise Exception('101')
    else:
        if action_dict['type'] == ActType.SaveCommand:
            user_msg = action_dict['data'].format(text_message=getRandomInput(), data=server_data)
            user_messages.append(user_msg)
            data_name = action_dict['save_to_data_name']
            server_data[data_name] = user_msg.format(text_message=user_msg, data=server_data)
        else:
            raise Exception('102')

    if 'next_act_id' in action_dict:
        next_act_message = getSequenceFromActDict(action_dict['next_act_id'], server_data=server_data)
        for user_msg in next_act_message['texts']:
            user_messages.append(user_msg)
        for server_msg in next_act_message['responses']:
            server_messages.append(server_msg)

    elif 'follow_up_act_id' in action_dict:
        follow_up_act_message = getSequenceFromActDict(action_dict['follow_up_act_id'],
                                                       server_data=server_data, is_follow_up=True)
        for user_msg in follow_up_act_message['texts']:
            user_messages.append(user_msg)
        for server_msg in follow_up_act_message['responses']:
            server_messages.append(server_msg)

    return {'texts': user_messages, 'responses': server_messages}


def getRandomInput():
    return NamesTemplates[randint(0, len(NamesTemplates)-1)]


NamesTemplates = ['ido', 'nadav', 'gal', 'ben', 'alon', 'adi', 'omer', 'inbal', 'shir', 'dor']

message_sequences = [
    {'texts': ['q1', 'cookie'],
     'responses': ['what is your nickname?', 'now your nickname will be cookie']
     },
    {'texts': ['okay', 'ok', 'OK', 'Ok'],
     'responses': ['OK', 'OK', 'OK', 'OK']
     },
]
