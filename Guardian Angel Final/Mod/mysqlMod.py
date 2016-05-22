
import mysql.connector
import time


"""
    connects to the database and updates it with information about the new event
"""
class mysqlMod():
    def __init__(self):
        None

    def updateDb(self, vid, id, msg):
        cnx = mysql.connector.connect(user='raspberry', password='g', host='#.#.#.#', database='raspberry')
        cursor = cnx.cursor()
        sql = "update testvideo set video='" + vid + ".avi', msg='" + msg + "', tid='" + time.strftime("%Y/%m/%d %H:%M:%S") +"' where id=" + str(id)
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
