import mysql.connector
import pymysql
import jdatetime
import database as db
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

"""This method returns list of dictionaries that contains reports that didn't noticed"""
def get_recent_reports():
    query = """
    SELECT * 
    FROM reports 
    WHERE status = 0
    """
    cursor.execute(query)
    results = cursor.fetchall()

    list = []
    for i in results:
        dic = {}
        report_id, user_id, text, city, date, status, alias = i
        dic['report_id'] = report_id
        dic['user_id'] = user_id
        dic['text'] = text
        dic['city'] = city
        dic['date'] = date
        dic['status'] = status
        dic['alias'] = alias
        list.append(dic)

    return list
    
def reject_report(report_text):
    report_text = report_text.split('\n __________________')[0]
    report_text = report_text.strip("")
    # user_id = int(user_id)
    print(f"\n\n\n {report_text}\n\n\n")

    query = f"""
    UPDATE reports
    SET status = -1
    WHERE report_text = '{report_text}' AND status = 0
    
    """
    cursor.execute(query)
    db.commit()
    bot_functions.tell_user_for_reject(report_text)

    

    
