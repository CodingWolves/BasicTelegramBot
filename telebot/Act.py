from abc import ABC, abstractmethod
from telegram.bot import Bot
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from telebot.credentials import bot_user_name, URL
from telebot.ActDict import *

global Acts


def InitializeActs():
    print("<<<<<<<<<<!!!Acts Created!!!>>>>>>>>>>")
    global Acts
    Acts = [Act.CreateAct(act_dict) for act_dict in ActionsDictionary]


class Act(ABC):
    @classmethod
    def CreateAct(cls, act: dict):
        print("Creating Act {}".format(act['id']))
        if act['type'] == ActType.Text:
            return TextResponse(act)
        elif act['type'] == ActType.Animation:
            return AnimationResponse(act)
        elif act['type'] == ActType.SaveCommand:
            return SaveCommand(act)

    @classmethod
    def getActByTrigger(cls, trigger):
        for act in Acts:
            if act.isTriggeredBy(trigger):
                return act
        print("did not find an Act for trigger {trigger}".format(trigger=trigger))

    @classmethod
    def getActById(cls, act_id):
        for act in Acts:
            if act.id == act_id:
                act: Act
                return act

    def __init__(self, act: dict):
        self.original_dict = act
        self.id = act['id']
        self.triggers = act['triggers']
        self.data = act['data']
        self.markup = None

        self.follow_up_act_id = None
        if 'follow_up_act_id' in act:
            self.follow_up_act_id = act['follow_up_act_id']

        self.next_act_id = None
        if 'next_act_id' in act:
            self.next_act_id = act['next_act_id']

        if 'markup_type' in act:
            markup_type = act['markup_type']

            if 'markup_data' in act:
                markup_string = act['markup_data']
                options = [[item for item in row.split(",")] for row in
                           markup_string.split(":")]  # convert it to lists in list

                if markup_type == MarkupType.OneTimeReply:
                    self.markup = ReplyKeyboardMarkup(options, one_time_keyboard=True)
                if markup_type == MarkupType.StaticReply:
                    self.markup = ReplyKeyboardMarkup(options)

            elif act['markup_type'] == MarkupType.Remove:
                self.markup = ReplyKeyboardRemove()
            else:
                print('error 15')  # act is not correct , markup_type exist and not 'Remove' but no markup_data
                pass
        pass

    def isTriggeredBy(self, text: str) -> bool:
        return text in self.triggers

    @abstractmethod
    def doAct(self, bot: Bot, chat, message):
        result = None
        if self.follow_up_act_id:
            print("follow_up_act_id has been sent - {follow_up_act_id} from act - {act_id}".format(
                follow_up_act_id=self.follow_up_act_id, act_id=self.id))
            result = Act.getActById(self.follow_up_act_id)
        if self.next_act_id:
            print("next_act has been sent - {next_act_id} from act - {act_id}".format(next_act_id=self.next_act_id,
                                                                                      act_id=self.id))
            result = Act.getActById(self.next_act_id).doAct(bot, chat, message)
        print("sending")
        print(result)
        print("sent")
        return result


class TextResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        format_names = getFormatNames(self.data)
        print('found formant_name ')
        print(format_names)
        print("chat.data")
        print(chat.data)
        for name in format_names:
            if name.split('.')[1] not in chat.data:
                print("error - trying to find {format_name} in chat.data but not found , chat_id={chat_id}".format(format_name=name, chat_id=chat.id))
                return
        text = self.data.format(user=chat.user, data=chat.data, bot_user_name=bot_user_name)
        if text == "":
            print("error - act id {} tried sending a null text".format(self.id))
            return
        bot.sendMessage(chat_id=chat.id, text=text,
                        reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(TextResponse, self).doAct(bot, chat, message)

    pass


class AnimationResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        url = self.data.format(URL=URL)
        if url == "":
            print("act id {} tried sending a null url animation".format(self.id))
            return
        bot.sendAnimation(chat_id=chat.id, animation=url,
                          reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(AnimationResponse, self).doAct(bot, chat, message)
        pass

    pass


class PhotoResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        return super(PhotoResponse, self).doAct(bot, chat, message)
        pass

    pass


class Command(Act):
    def __init__(self, act: dict):
        super(Command, self).__init__(act)
        pass

    pass


class SaveCommand(Command):  # command cannot change chat.data from this scope , it only get a shadow chat
    def __init__(self, act: dict):
        super(SaveCommand, self).__init__(act)
        act_data = self.data.split('=')
        self.data_name = act_data[0]
        self.value = act_data[1]
        self.caller_act = act

    def doAct(self, bot: Bot, chat, message):
        text_message = GetTextFromMessage(message)
        chat.data[self.data_name] = self.value.format(text_message=text_message)
        print("data has been changed  ,,,  chat_id - {chat_id} , data_name - {data_name} , text_message={text_message}"
              .format(chat_id=chat.id, data_name=self.data_name, text_message=text_message))
        print(chat.data[self.data_name])
        return super(SaveCommand, self).doAct(bot, chat, message)


def GetTextFromMessage(message):
    return message.text.encode('utf-8').decode()


def getFormatNames(text):
    names = []
    start_index = text.find('{')
    end_index = text.find('}', start_index)
    while start_index != -1 and end_index != -1:
        names.append(text[start_index:end_index + 1])
        text = text[:start_index] + text[end_index + 1:]
        start_index = text.find('{')
        end_index = text.find('}', start_index)
    return names
