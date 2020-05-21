from abc import ABC, abstractmethod
from telegram.bot import Bot
from telegram.replykeyboardremove import ReplyKeyboardRemove


class Act(ABC):
    @classmethod
    def CreateAct(cls, act: dict):
        print("Creating Act {}".format(act['id']))
        if act['type'] == 'text':
            return TextResponse(act)

    def __init__(self, act: dict):
        self.id = act['id']
        self.triggers = act['triggers']
        self.data = act['data']
        if 'markup' in act:
            self.markup = act['markup']
        else:
            self.markup = ReplyKeyboardRemove()
        pass

    def isTriggeredBy(self, text: str) -> bool:
        return text in self.triggers

    @abstractmethod
    def doAct(self, bot: Bot, chat, message):
        pass


class TextResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        bot.sendMessage(chat_id=chat.id, text=self.data,
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
