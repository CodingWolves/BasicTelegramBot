import telegram

from telebot.credentials import bot_user_name, URL
from telebot.Act import Act
from telebot.Generic import Object

from time import sleep


class Chat:
    def __init__(self, message):
        self.id = message.chat.id
        self.user = {
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name,
        }
        self.data = Object()
        self.follow_up_act = False
        self.unhandled_messages = []

    def GotMessage(self, bot, message):
        text = message.text.encode('utf-8').decode()
        print("chat - {chat_id} got text_message = {text_message}".format(chat_id=self.id, text_message=text))
        print("chat continue , follow_up_act={follow_up_act}".format(follow_up_act=self.follow_up_act))
        if self.follow_up_act:
            print("found previous follow_up_act {id} , now acting".format(id=self.follow_up_act.id))
            self.follow_up_act = self.follow_up_act.doAct(bot, self, message)
            return
            pass

        print("after follow_up_act")

        act = Act.getActByTrigger(text)
        if issubclass(type(act), Act):
            print("doing act - {id} after text = {text}".format(id=act.id, text=text))
            follow_up_act = act.doAct(bot, self, message)
            if follow_up_act:
                print("got follow_up_act - {act_id}".format(act_id=follow_up_act.id))
                self.follow_up_act = follow_up_act
                print("setting as Chat.follow_up_act - now follow up id is {}".format(self.follow_up_act.id))

        print("end GotMessage")
