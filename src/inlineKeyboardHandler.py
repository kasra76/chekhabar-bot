from admin_server import AdminMessage
# import admin_database as db
import admin_database
import database
import bot_functions

class InLineKeyboardHandler():
    def __init__(self, message):
        self.message = message
    
    def execute(self):
        admin_id, callback_data, messageText, file_id, type = self.parseMessage()

        admin_message = AdminMessage(admin_id)
        if callback_data == "1":        
            request_json = admin_message.send_message_to_channel(messageText, type, file_id)
            report_text = messageText.split('\n __________________')[0]
            report_text = report_text.strip("")
            user_id = database.get_userid_from_report(report_text)
            if user_id:
                database.add_message_id_to_reports(request_json, user_id, report_text)
                bot_functions.tell_user_for_acc(report_text)
                database.add_coin(user_id, 1)

        
        elif callback_data == "2":
            print("\n\n\n reject report \n\n\n")
            admin_database.reject_report(messageText)
        elif callback_data == "4":
            print("\n\n\n vegetable doing \n\n\n")


    def parseMessage(self):
        callback_data = self.message['callback_query']['data']
        user_id = self.message['callback_query']['from']['id']

        if 'text' in self.message['callback_query']['message'].keys():
            text = self.message['callback_query']['message']['text']
            file_id = None
            type = 1
        elif 'photo' in self.message['callback_query']['message'].keys():
            text = self.message['callback_query']['message']['caption']
            file_id = self.message['callback_query']['message']['photo'][0]['file_id']
            type = 2
        elif 'video' in self.message['callback_query']['message'].keys():
            text = self.message['callback_query']['message']['caption']
            file_id = self.message['callback_query']['message']['video']['file_id']
            type = 3
 
        return (user_id, callback_data, text, file_id, type)