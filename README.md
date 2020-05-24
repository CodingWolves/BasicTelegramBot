# BasicTelegramBot

this telegram bot is a template based bot that can be more easly configured to your needs

# ActDict

ActionsDictionary is a list of dictionaries that represent the templates availiable for responses

- 'id' identification for follow up and next acts
- 'triggers' is a list of possible triggers that activate this action
- 'next_act_id' is the next imidiate act to do after completing this one
- 'follow_up_act_id' is the next act to do no matter what the user sends , like asking what is your name, then the 'follow_up_act_id' value will point to an action that saves the message the user sent after the question
- 'data' this value is formated with {data} and {text_message}. 
	- If there is {text_message} inside of 'data' it will get the last message sent from the user
	- If there is saved data name in chat for 'nickname' if u use {data.nickname} inside of data, it will get you the saved value of it
- 'type' controls what to do with 'data' after format
	- ActType.Text			= sends a message back
	- ActType.Animation		= sends an animation back (needs url)
	- ActType.SaveCommand		= data is saved to variable name thats written in 'save_to_data_name' in chat

- markup is the list of potential responses that the user can input by pressing a button
	- 'markup_type'
		- MarkupType.StaticReply 	= shows the user a list of potential responses forever
		- MarkupType.OneTimeReply	= shows the user a list of potential responses but after the user select one it disapears
		- MarkupType.Remove			- removes the previous set markup, mainly use for removing MarkupType.StaticReply
				
	- 'markup_data'	- list of potential responses in format ',' will seperate between values and ':' will seperate between rows example "row1_item1,row1_item2:row2_item3"

- 'evaluate' uses eval function on 'data' and saves to 'save_to_data_name' variable name



# Act

Here are all the classes that use the telegram.Bot to send messages

InitializeActs method creates all the possible actions after reading them from the ActDict variable(ActionsDictionary)

To find the correct action to do after getting a message, use getActByTrigger.




