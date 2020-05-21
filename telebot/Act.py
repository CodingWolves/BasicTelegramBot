from abc import ABC, abstractmethod
from telegram.bot import Bot
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from telebot.credentials import bot_user_name, URL
from telebot.ActDict import MarkupType, ActType


class Act(ABC):
    @classmethod
    def CreateAct(cls, act: dict):
        print("Creating Act {}".format(act['id']))
        if act['type'] == ActType.Text:
            return TextResponse(act)

    def __init__(self, act: dict):
        self.id = act['id']
        self.triggers = act['triggers']
        self.data = act['data']
        self.markup = None
        if 'markup_type' in act:
            markup_type = act['markup_type']

            if 'markup_data' in act:
                markup_string = act['markup_data']
                options = [[item for item in row.split(",")] for row in markup_string.split(":")]  # convert it to lists in list

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
        pass


class TextResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        text = self.data.format(user=chat.user, bot_user_name=bot_user_name)
        bot.sendMessage(chat_id=chat.id, text=text,
                        reply_to_message_id=message.message_id, reply_markup=self.markup)
        pass

    pass


class PhotoResponse(Act):
    def __init__(self, act: dict):
        Act.__init__(self, act)
        self.url = self.data

    def doAct(self, bot: Bot, chat, message):
        pass

    pass


class AnimationResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        pass

    pass


class SaveResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        pass

    pass


class QuestionResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        pass

    pass
