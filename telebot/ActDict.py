class ActType:
    Text = 'text'
    Animation = 'animation'
    SaveCommand = 'save_command'


class MarkupType:
    OneTimeReply = 'reply'
    StaticReply = 'static_reply'
    Remove = 'remove'


ActionsDictionary = [
    {
        'id': 1,
        'triggers': ['/start', 'start'],
        'type': ActType.Text,
        'data': """
                Welcome to coolAvatar bot, 
                the bot is using the service from http://avatars.adorable.io/ 
                to generate cool looking avatars based on the name you enter 
                so please enter a name and the bot will reply with an avatar for your name.
        """
    },
    {
        'id': 2,
        'triggers': ['hi', 'hello', 'hey'],
        'type': ActType.Text,
        'data': 'hello to you too'
    },
    {
        'id': 1000,
        'triggers': ['ok', 'okay', 'OK', 'Ok'],
        'type': ActType.Text,
        'data': 'OK'
    },
    {
        'id': 1001,
        'triggers': ['bye', 'bye bye', 'byebye', ''],
        'type': ActType.Animation,
        'data': '{URL}bye_bye'
    },
    {
        'id': 2001,
        'triggers': ['whats my name?', 'what is my name?'],
        'type': ActType.Text,
        'data': 'your name is {user.first_name}'
    },
    {
        'id': 2002,
        'triggers': ['whats my nickname?', 'what is my nickname?', 'my nickname?'],
        'type': ActType.Text,
        'data': 'your name is {data.nickname}'
    },
    {
        'id': 3001,
        'triggers': ['options2', ''],
        'type': ActType.Text,
        'data': 'options static',
        'markup_type': MarkupType.StaticReply,
        'markup_data': "hi,bye:hi2,bye2"
    },
    {
        'id': 3002,
        'triggers': ['options', '/help'],
        'type': ActType.Text,
        'data': 'options one time',
        'markup_type': MarkupType.OneTimeReply,
        'markup_data': "hi,bye:hi2,bye2"
    },
    {
        'id': 9998,
        'triggers': ['q1', 'question 1', 'question number 1'],
        'type': ActType.Text,
        'data': 'what is your nickname?',
        'markup_type': MarkupType.Remove,
        'follow_up_act_id': 9999
    },
    {
        'id': 9999,
        'triggers': [],
        'type': ActType.Command,
        'data': 'nickname={text_message}',
    },
    {
        'id': 10000,
        'triggers': ['reset nickname'],
        'type': ActType.Command,
        'data': 'nickname=',
    },
    {
        'id': 10100,
        'triggers': ['calc', 'calculate'],
        'type': ActType.Command,
        'data': 'enter your equation now',
    }

]
