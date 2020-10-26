import database as db

class Semaphore:
    def __init__(self):
        self.current_state = 0
    
    def is_ligal(self, content, user_id, state):
        self.user_id = user_id
        self.current_state = state

        if state == 0:
            return self.state0(content)
        elif state == 1:
            return self.state1(content)
        elif state == 2:
            return self.state2(content)
        elif state == 3:
            return self.state3(content)
        elif state == 4:
            return self.state4(content)
        elif state == 5:
            return self.state5(content)
        elif state == 6:
            return self.state6(content)
        elif state == 7:
            return self.state7(content)
        elif state == 8:
            return self.state8(content)
        elif state == 9:
            return self.state9(content)
        elif state == 10:
            return self.state10(content)
        elif state == 11:
            return self.state11(content)
        elif state == 12:
            return self.state12(content)
        elif state == 13:
            return self.state13(content)
        elif state == 14:
            return self.state14(content)
        elif state == 15:
            return self.state15(content)
        elif state == 16:
            return self.state16(content)
        elif state == 17:
            return self.state17(content)
        elif state == 18:
            return self.state18(content)
        elif state == 19:
            return self.state19(content)
        elif state == 20:
            return self.state13(content)
        elif state == 21:
            return self.state21(content)
        elif state == 22:
            return self.state22(content)
        elif state == 23:
            return self.state23(content)
        elif state == 24:
            return self.state24(content)
        

    def state0(self, content):
        if content == "start":
            return True
        elif content == "\U0000274C تمایلی ندارم":
            return True
        else:
            return False

    
    def state1(self, content):
        if content == '\U0000274C تمایلی ندارم':
            return True
        elif content == 'start':
            return True
        else:
            return False

    def state2(self, content):
        if content == "شروع مجدد":
            return True
        elif content == "start":
            return True
        else:
            return False
    
    """منو اصلی"""
    def state3(self, content):
        if content == "📝 ارسال گزارش" :
            return True
        elif content == "❓ قوانین و راهنما":
            return True
        elif content == "👤 پروفایل":
            return True
        elif content == "😉 سبزی پاک کنیم":
            return True
        elif content == "start":
            return True
        else: 
            return False

    """👤 پروفایل"""
    def state4(self, content):
        if content == "💰 امتیازات":
            return True
        elif content == "📕 تاریخجه گزارش ها":
            return True
        elif content == "\U0001F465 افزودن نام مستعار جدید":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False
        
    """💰 امتیازات"""
    def state5(self, content):
        if content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == 'start':
            return True
        else:
            return False


    """📕 تاریخجه گزارش ها"""
    def state6(self, content):
        if content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False
    
    """اایجاد نام مستعار جدید"""
    def state7(self, content):
        return True
    

    """رمانی که نام مستعار جدید نتوان ساخت"""
    def state8(self, content):
        if content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == 'start':
            return True
        else:
            return False
    

    """گرینه چهارم"""
    def state9(self, content):
        return True

    
    """📝 ارسال گزارش"""
    def state10(self, content):
        if content == "انتخاب نام مستعار":
            print("\n\npocker face1\n\n")               
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == 'start':
            return True
        else:
            return False
    
    """انتخاب نام مستعار"""
    def state11(self, content):
        aliases = db.get_aliases(self.user_id)
        if content in aliases:
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == 'start':
            return True
        else:
            return False


    """ایجاد نام مستعار جدید در زمان ارسال گزارش"""
    def state12(self, content):
        return True

    """آنتخاب شهر"""
    def state13(self, content):
        num_list = ['1', '2', '3']
        if content in num_list:
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False
    
    """ارسال گزارش"""
    def state14(self, content):
        return True
    
    """راهنما و قوانین"""
    def state15(self, content):
        if content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False
    
    def state16(self, content):
        if content == "شروع":
            return True
        elif content == "start":
            return True
        else:
            return False

    def state17(self, content):
        if content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False

    """تایید انتخاب شهر و رفتن به سمت نوشتن گزارش"""
    def state18(self, content):
        if content == "\U00002712 نوشتن گزارش":
            return True
        elif content == '\U000027A1 بازگشت به منو اصلی':
            return True
        elif content == 'start':
            return True
        else:
            return False
    
    """ـایید ارسال گزارش"""
    def state19(self, content):
        if content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            return False

    """تایید انتخاب نام مستعار و رفتن به سمت انتخاب شهر"""
    def state20(self, content):
        if content == "انتخاب شهر رخداد":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "start":
            return True
        else:
            False


    def state21(self, content):
        if content == "start":
            return True
        elif content == "help":
            return True
        elif content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        else: 
            return False
    

    def state22(self, content):
        return True

    def state23(self, content):
        if content == "start":
            return True
        elif content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "help":
            return True
        else:
            return False
        
    
    def state24(self, content):
        if content == "start":
            return True
        elif content == "\U000021AA بازگشت به پروفایل":
            return True
        elif content == "\U000027A1 بازگشت به منو اصلی":
            return True
        elif content == "help":
            return True
        else:
            return False