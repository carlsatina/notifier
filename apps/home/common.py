# -*- encoding: utf-8 -*-
import mysql.connector
from decouple import config
import requests, json

class UserData():
    def __init__(self):

        #db_client = mysql.connector.connect(host="r1bsyfx4gbowdsis.cbetxkdyhwsb.us-east-1.rds.amazonaws.com", user="lary6u2vifyxhf68", passwd="f1o0lpb082k1auo8", database="byb0h4mglwort2e7", ssl_ca="./rds-combined-ca-bundle.pem")
        self.db_client = mysql.connector.connect(
            host=config('DB_HOST'),
            user=config('DB_USER'),
            passwd=config('DB_PASSWORD'),
            database=config('DB_NAME'),
            ssl_ca=config('DB_SSL_CA_PATH'))

        self.db_cursor = self.db_client.cursor(dictionary=True)
        self.db_cursor.execute("select distinct * from rg_users left join rg_user_security on rg_users.user_id = rg_user_security.user_id")
        self.rows = self.db_cursor.fetchall()

    def fetch_all(self):
        return self.rows

    def fetch_with_user_id(self, user_id):
        # select_statement = "select rg_users.user_id, rg_users.name, rg_users.email, rg_users.postcode, rg_user_security.push_notif_token "
        # select_statement += "from rg_users, rg_user_security "
        # select_statement += "where rg_users.user_id = " + str(user_id) + " and rg_user_security.user_id = " + str(user_id)

        # self.db_cursor.execute(select_statement)
        # user = self.db_cursor.fetchall()
        for user in self.rows:
            if user['user_id'] == user_id:
                return user

        return None

    def close(self):
        self.db_cursor.close()
        self.db_client.close()


class Notifier():
    def __init__ (self):

        self.url = "https://exp.host/--/api/v2/push/send"
        self.headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate'
        }

    def send_notification(self, data):

        if len(data) > 1:
            # Send Multiple
            print ('multiple data: ', data)
            r = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        else:
            # Send Single
            r = requests.post(self.url, data=json.dumps(data[0]), headers=self.headers)


