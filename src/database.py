import mysql.connector
import pymysql
import jdatetime
import datetime
import bot_functions

db = mysql.connector.connect(
    host='localhost',
    user='chekhabar-bot',
    passwd='4u]]Q@tG?NQ<,zqp',
    database='chekhabar-bot'
)

# db = pymysql.connect(
#     host='localhost',
#     user='root',
#     passwd='!+MayaTech+!',
#     database='chekhabar'
# )

cursor = db.cursor()

def create_user_table():    
    query = 'CREATE TABLE users(user_id int NOT NULL PRIMARY KEY ON DELETE CASCADE, phone_number int, alias1 VARCHAR(255), alias2 VARCHAR(255), alias3 VARCHAR(255))'
    cursor.execute(query)


def create_scores_table():
    query = "CREATE TABLE scores(user_id int NOT NULL , coin int NOT NULL, cash int NOT NULL, FOREIGN KEY(user_id) REFERENCES users(user_id))"
    cursor.execute(query)


def create_reports_table():
    query = "CREATE TABLE reports(report_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id int NOT NULL, report_text text NOT NULL, city VARCHAR(255), FOREIGN KEY(user_id) REFERENCES users(user_id))"
    cursor.execute(query)

# TODO : just for debugging purposes => before adding a user, check for existance of that users
def add_user(user_id, phone_number, firstname, lastname, username):
    find = search_userId(user_id)
    if find == -1:
        query = "INSERT INTO users (user_id, phone_number, alias1, alias2, alias3, firstname, lastname, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, phone_number, None, None, None, firstname, lastname, username)
        cursor.execute(query, values)
        db.commit()


    find2 = search_scoreID(user_id)
    if find2 == -1:
        query2 = 'INSERT INTO scores (user_id, coin, cash) VALUES (%s, %s, %s)'
        values2 = (user_id, 0, 0)
        cursor.execute(query2, values2)
        db.commit()
    
    find3 = search_stateID(user_id)
    if find3 == -1:
        query3 = "INSERT INTO state (user_id, last_state) VALUES (%s, %s)"
        values3 = (user_id, 1)
        cursor.execute(query3, values3)
        db.commit()
    
    return 3



def update_phoneNumber(user_id, phone_number):
    query = "UPDATE users SET phone_number = {} WHERE user_id = {}".format(phone_number, user_id)
    cursor.execute(query)
    db.commit()


def update_alias(user_id, alias, index):
    query = "UPDATE users SET alias{} = {} WHERE user_id = {}".format(index, alias, user_id)
    cursor.execute(query)
    db.commit()



def get_coins(user_id):
    query = f"SELECT coin, cash FROM scores WHERE user_id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_cash(user_id):
    query = f"SELECT cash FROM scores WHERE user_id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()


def add_coin(user_id, value):
    get_query = "SELECT coin FROM scores WHERE user_id = {}".format(user_id)
    cursor.execute(get_query)
    record = cursor.fetchall()
    primitive_value, = record[0]
    secondary_value = primitive_value + value

    set_query = "UPDATE scores SET coin = {} WHERE user_id = {}".format(secondary_value, user_id)
    cursor.execute(set_query)
    db.commit


def add_cash(user_id, value):
    get_query = "SELECT cash FROM scores WHERE user_id = {}".format(user_id)
    cursor.execute(get_query)
    record = cursor.fetchall()
    primitive_value = record[0]
    secondary_value = primitive_value + value

    set_query = "UPDATE scores SET cash = {} WHERE user_id = {}".format(secondary_value, user_id)
    cursor.execute(set_query)
    db.commit



"""This function uses when a user wants to pay for a private chat or other services
    Return:
        -1 when he does not have enough coin
        1 when he have enough coin to pay from"""
def sub_coin(user_id, value):
    get_query = "SELECT coin FROM scores WHERE user_id = {}".format(user_id)
    cursor.execute(get_query)
    record = cursor.fetchall()
    primitive_value = record[0]

    if primitive_value < value:
        return -1
    else:
        secondary_value = primitive_value - value
        set_query = "UPDATE scores SET coin = {} WHERE user_id = {}".format(secondary_value, user_id)
        cursor.execute(set_query)
        db.commit()
        return 1

    
"""This function uses when a user wants to pay for a private chat or other services
    Return:
        -1 when he does not have enough coin
        1 when he have enough coin to pay from"""
def sub_cash(user_id, value):
    get_query = "SELECT cash FROM scores WHERE user_id = {}".format(user_id)
    cursor.execute(get_query)
    record = cursor.fetchall()
    primitive_value = record[0]

    if primitive_value < value:
        return -1
    else:
        secondary_value = primitive_value - value
        set_query = "UPDATE scores SET cash = {} WHERE user_id = {}".format(secondary_value, user_id)
        cursor.execute(set_query)
        db.commit()
        return 1
        

def get_aliases(user_id):
    aliases = []
    query1 = f"SELECT alias1 FROM users WHERE user_id = {user_id}"
    query2 = f"SELECT alias2 FROM users WHERE user_id = {user_id}"
    query3 = f"SELECT alias3 FROM users WHERE user_id = {user_id}"

    cursor.execute(query1)
    res1 = cursor.fetchall()
    if len(res1) == 0 or (len(res1) == 1 and res1[0] == (None,)):
        pass
    else:
        t_alias,  = res1[0]
        aliases.append(t_alias)
    
    cursor.execute(query2)
    res2 = cursor.fetchall()
    if len(res2) == 0 or (len(res2) == 1 and res2[0] == (None,)):
        pass
    else:
        t_alias, = res2[0]
        aliases.append(t_alias)

    cursor.execute(query3)
    res3 = cursor.fetchall()
    if len(res3) == 0 or (len(res3) == 1 and res3[0] == (None,)):
        pass
    else:
        t_alias, = res3[0]
        aliases.append(t_alias)
    
    return aliases


"""
    Retrun : 1 if user found
            -1 if user not found"""
def search_userId(user_id):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        return -1
    else:
        return 1


def search_scoreID(user_id):
    query = f"SELECT * FROM scores WHERE user_id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        return -1
    else:
        return 1


def search_stateID(user_id):
    query = f"SELECT * FROM state WHERE user_id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        return -1
    else:
        return 1
        


def delete_user(user_id):
    query2 = f"DELETE FROM scores WHERE user_id = {user_id}"
    cursor.execute(query2)
    query3 = f"DELETE FROM state WHERE user_id = {user_id}"
    cursor.execute(query3)
    query4 = f"DELETE FROM alias_city_cache WHERE user_id = {user_id}"
    cursor.execute(query4)
    query5 = f"DELETE FROM reports WHERE user_id = {user_id}"
    cursor.execute(query5)
    query = f"DELETE FROM users WHERE user_id = {user_id}"
    cursor.execute(query) 
    db.commit()


def get_state(user_id):
    query = f"SELECT last_state FROM state WHERE user_id = {user_id}"
    cursor.execute(query)
    state = cursor.fetchall()
    # state = [(0,)]
    return state



def update_state(user_id, state):
    print(f"\n\n\n beggining of update_state\n user_id = {user_id}\nstate = {state}\n\n\n")
    query = f'UPDATE state SET last_state = {state} WHERE user_id = {user_id}'
    cursor.execute(query)
    db.commit()
    print("\n\n\n end of update_state")


def add_alias(user_id, alias, num):
    num = str(num)
    query = f'UPDATE users SET alias{num} = "{alias}" WHERE user_id = {user_id}'
    cursor.execute(query)
    db.commit()


def insert_report(user_id, content, message_id, file_id=None):
    print("\n\n\n database inser report \n\n\n")
    query = "INSERT INTO reports (user_id, report_text, city, date_time, status, alias, channel_message_id, message_id, file_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    date_time = datetime.datetime.now()
    status = 0
    cached_data = get_aliasAndCity_from_cache(user_id)
    if len(cached_data) > 0:
        alias, city = get_aliasAndCity_from_cache(user_id)[0]
        values = (user_id, content, city, date_time, status, alias, None, message_id, file_id)
        cursor.execute(query, values)
        return (city, alias)


def cache_alias(user_id, alias):
    print("\n\n alias cached \n\n")
    query = "INSERT INTO alias_city_cache (user_id, alias, city) VALUES (%s, %s, %s)"
    values = (user_id, alias, None)
    cursor.execute(query, values)
    db.commit()
    print("\n\n caching alias done \n\n")

def cache_city(user_id, city_number):
    print("\n\n city cached \n\n")
    query = f"""
    UPDATE alias_city_cache 
    SET city = {city_number}
    WHERE user_id = {user_id}
    """
    cursor.execute(query)
    db.commit()


def empty_cache(user_id):
    query = f"""
    DELETE FROM alias_city_cache
    WHERE user_id = {user_id}
    """
    cursor.execute(query)
    db.commit()


def get_aliasAndCity_from_cache(user_id):
    query = f"""
    SELECT alias, city
    FROM alias_city_cache
    WHERE user_id = {user_id}
    """

    cursor.execute(query)
    return cursor.fetchall()



def drop_cache(user_id):
    query = f"""
    DELETE FROM alias_city_cache
    WHERE user_id = {user_id}
    """
    cursor.execute(query)
    db.commit()


def get_admins():
    query = """
    SELECT user_id
    FROM admins
    """
    cursor.execute(query)
    admins = cursor.fetchall()
    admin_list = []
    for admin in admins:
        id, = admin
        admin_list.append(id)
    return admin_list



def add_to_waiting_reports(user_id, text):
    query = """
    INSET INTO waiting_reports
    (user_id, text) VALUES (%s, %s)
    """
    values = (user_id, text)
    cursor.execute(query, values)
    db.commit()




def test_check_report_text(text):
    query = f"""
    SELECT report_id, user_id, status
    FROM reports
    WHERE report_text = '{text}'
    """
    cursor.execute(query)
    reports = cursor.fetchall()
    print(reports)



def add_message_id_to_reports(request, user_id, report_text):
    print(f"\n\n\n {request} \n\n\n")
    print("\n\n\nreport_text = {}\nuser_id = {}\n\n\n".format(report_text, user_id))
    message_id = int(request['result']['message_id'])
    query = f"""
    UPDATE reports 
    SET channel_message_id = {message_id}
    WHERE user_id = {user_id} AND report_text = '{report_text}'
    """
    cursor.execute(query)
    db.commit()


def get_report_message_id(report_text):
    query = f"""
    SELECT user_id, message_id
    from reports
    WHERE report_text = '{report_text}' AND status = 0
    """
    cursor.execute(query)
    reports = cursor.fetchall()
    if len(reports) > 0:
        user_id, message_id = reports[0]
        return user_id, message_id
    else:
        return None, None


def get_userid_from_report(report_text):
    query = f"""
    SELECT user_id
    from reports
    WHERE report_text = '{report_text}' AND status = 0
    """
    cursor.execute(query)
    ids = cursor.fetchall()
    if len(ids) > 0:
        user_id, = ids[0]
        return user_id
    else:
        return None


def get_report_userid_message_id_for_reject(report_text):
    query = f"""
    SELECT user_id, message_id
    from reports
    WHERE report_text = '{report_text}' AND status = -1
    """
    cursor.execute(query)
    reports = cursor.fetchall()
    if len(reports) > 0:
        user_id, message_id = reports[0]
        return user_id, message_id
    else:
        return None, None
