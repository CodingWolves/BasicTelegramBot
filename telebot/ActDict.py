class ActType:
    Text = 'text'
    Animation = 'animation'


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
        'id': 3001,
        'triggers': ['options2', ''],
        'type': ActType.Text,
        'data': 'options static',
        'markup_type': MarkupType.StaticReply,
        'markup_data': "hi,bye:hi2,bye2"
    },
    {
        'id': 3002,
        'triggers': ['options', ''],
        'type': ActType.Text,
        'data': 'options one time',
        'markup_type': MarkupType.OneTimeReply,
        'markup_data': "hi,bye:hi2,bye2"
    },
    {
        'id': 0,
        'triggers': ['', ''],
        'type': ActType.Text,
        'data': ''
    },
]
