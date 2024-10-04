WELCOME_MSG = "Hello! Welcome to my chatbot!"
MY_NEW_TOKEN_SET_MSG = lambda me: f"Your new user token:\n{me}"
MY_TOKEN_MSG = lambda me: f"Your token:\n{me}"
MY_TOKEN_NOT_FOUND_MSG = "Token was not found."
SET_RECIPIENT_MSG = "Please, enter new Recipient's token."
SET_RECIPIENT_PLACEHOLDER = "Recipient's token"
NEW_RECIPIENT_MSG = lambda recipient: f"Your recipient now is: {recipient}."
RECIPIENT_DELETE_MSG = "Your recipient was set to null."
GET_RECIPIENT_MSG = lambda recipient: f"Your recipient is: {recipient}"
INCOMING_MESSAGE_MSG = lambda sender, text: f"⚠️ INCOMING MESSAGE FROM {sender}:\n{text}\n----END OF TRANSMISSION----"
MESSAGE_SENT_MSG = lambda recipient: f"Your message has been sent to {recipient}."
RECIPIENT_NOT_FOUND_MSG = lambda recipient: f"Recipient {recipient} was not found.\nYour message has NOT been sent."
