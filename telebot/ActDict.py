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
        'triggers': ['bye', 'bye bye', 'byebye'],
        'type': ActType.Animation,
        'data': '{URL}bye_bye'
    },
    {
        'id': 2001,
        'triggers': ['whats my name?', 'what is my name?'],
        'type': ActType.Text,
        'data': 'your name is {data.user.first_name}'
    },
    {
        'id': 2002,
        'triggers': ['whats my nickname?', 'what is my nickname?', 'my nickname?'],
        'type': ActType.Text,
        'data': 'your name is {data.nickname}'
    },
    {
        'id': 3001,
        'triggers': ['options2'],
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
        'id': 5001,
        'triggers': ['q1', 'question 1', 'question number 1'],
        'type': ActType.Text,
        'data': 'what is your nickname?',
        'markup_type': MarkupType.Remove,
        'follow_up_act_id': 5002
    },
    {
        'id': 5002,
        'triggers': [],
        'type': ActType.SaveCommand,
        'data': '{text_message}',
        'save_to_data_name': 'nickname',
        'next_act_id':  5003
    },
    {
        'id': 5003,
        'triggers': [],
        'type': ActType.Text,
        'data': 'now your nickname will be {data.nickname}',
    },
    {
        'id': 5000,
        'triggers': ['reset nickname'],
        'type': ActType.SaveCommand,
        'data': '',
        'save_to_data_name': 'nickname'
    },
    {
        'id': 10100,
        'triggers': ['calc', 'calculate'],
        'type': ActType.Text,
        'data': 'enter your equation now',
        'follow_up_act_id': 10101
    },
    {
        'id': 10101,
        'triggers': [],
        'type': ActType.SaveCommand,
        'data': '{text_message}',
        'save_to_data_name': 'equation',
        'next_act_id': 10102
    },
    {
        'id': 10102,
        'triggers': [],
        'type': ActType.SaveCommand,
        'data': '{data.equation}',
        'save_to_data_name': 'equation_eval',
        'evaluate': True,
        'next_act_id': 10103
    },
    {
        'id': 10103,
        'triggers': [],
        'type': ActType.Text,
        'data': '{data.equation_eval}',
    }
]

need_to_add = [{
    'triggers': ['whats my name?', 'what is my name?'],
    'triggers': ['whats my name?', 'what is my name?'],
    'response': "{user.first_name}"
}, {
    'triggers': ['what is my full name?', 'whats my full name?'],
    'response': "{user.first_name} {user.last_name}"
}, {
    'triggers': ['what is my family name?', 'whats my family name?'],
    'response': "{user.last_name}"
}, {
    'triggers': ['whats your name?', 'what is your name?', 'what is ur name?', 'whats ur name?'],
    'response': "my name is {bot_user_name}"
}, {
    'triggers': ['i got options', 'options', 'option', 'what?', 'help', '/help'],
    'response': "options{ReplyMarkup:'hi','hello':'bye bye','whats your name?':"
                "'whats my full name?','ok':'inline options','/start'}"
}, {
    'triggers': ['inline options'],
    'response': "my options{InlineMarkup:'hi','hello':'bye bye','whats your name?':'whats my full name?'}"
},
]
