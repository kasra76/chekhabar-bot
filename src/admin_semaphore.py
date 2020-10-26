import admin_database

class Semaphore:
    def __init__(self):
        self.current_state = 101

    def is_ligal(self, content, user_id, state):
        self.user_id = user_id
        self.current_state = state

        if state == 101:
            return self.state101(content)
        elif state == 102:
            return self.state102(content)
        elif state == 103:
            return self.state103(content)

    
    def state101(self, content):
        if content == "\U0001F4EC مشاهده گزارش های اخیر":
            return True
        elif content == '\U0001F37F مشاهده چت های اخیر':
            return True
        elif content == '\U0001F575 اضافه کردن ادمین':
            return True
        elif content == '\U0001F5C3 ریز جزییات گزارش های امروز':
            return True
        elif content == 'start':
            return True
        elif content == 'help':
            return True
        else:
            return False

    
    def state102(self, content):
        if content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        elif content == "help":
            return True
        else:
            return False

    
    def state103(self, content):
        if  content == '\U000027A1 بازگشت به منو اصلی':
            return True
        elif content == "start":
            return True
        elif content == 'help':
            return True
        else:
            return False
