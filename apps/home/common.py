# -*- encoding: utf-8 -*-
import mysql.connector
from decouple import config

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
        self.db_cursor.execute("select * from rg_users left join rg_user_security on rg_users.user_id = rg_user_security.user_id")
        self.rows = self.db_cursor.fetchall()

    def fetch_all(self):
        return self.rows

    def close(self):
        self.db_cursor.close()
        self.db_client.close()