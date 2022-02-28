# -*- encoding: utf-8 -*-
import mysql.connector
from decouple import config
import requests, json

class UserData():
    """ 
    This class is responsible for connecting to the external database.
    """
    def __init__(self):

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
        for user in self.rows:
            if user['user_id'] == user_id:
                return user

        return None

    def close(self):
        self.db_cursor.close()
        self.db_client.close()


class Notifier():
    """ 
    This class is responsible for sending the notification via expo library/api.
    """
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
            r = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        else:
            # Send Single
            r = requests.post(self.url, data=json.dumps(data[0]), headers=self.headers)


