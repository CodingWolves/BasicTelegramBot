class ActType:
    Text = 'text'


class MarkupType:
    OneTimeReply = 'Reply'
    StaticReply = 'StaticReply'
    Remove = 'Remove'


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
        'id': 2001,
        'triggers': ['whats my name?', 'what is my name?'],
        'type': ActType.Text,
        'data': 'your name is {user.first_name}'
    },
    {
        'id': 3001,
        'triggers': ['options2', ''],
        'type': ActType.Text,
        'data': '',
        'markup_type': MarkupType.StaticReply,
        'markup_data': "hi,bye:hi2,bye2"
    },
    {
        'id': 0,
        'triggers': ['', ''],
        'type': ActType.Text,
        'data': ''
    },
]
