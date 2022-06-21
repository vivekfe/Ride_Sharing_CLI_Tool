import sqlite3
import os
from utils import pretty_print

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.create_database_if_not_exists()

    def create_database_if_not_exists(self):
        try:
            if os.path.exists(self.db_name):
                self.conn = sqlite3.connect(self.db_name)
                self.close_connection()
                self.conn = None
                return self
            else:
                self.conn = sqlite3.connect(self.db_name)
                pretty_print(f'Creating a new DB -> {self.db_name}')
                cursor = self.conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS RIDE_DETAILS
                                  (ride_date TEXT, driver_id INTEGER, ride_id INTEGER NOT NULL PRIMARY KEY, 
                                  time_taken INTEGER, distance INTEGER)''')

                cursor.execute('''CREATE TABLE IF NOT EXISTS DRIVER_RATING
                                  (driver_id INTEGER, ride_id INTEGER NOT NULL PRIMARY KEY, rating INTEGER)''')
                self.conn.commit()
                cursor.close()
                self.close_connection()
                pretty_print("DB has been created, closing existing connections")
                return self

        except sqlite3.Error as err:
            pretty_print('Database does not exist')
            pretty_print(err)


    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            pretty_print(f'Connected to existing DB -> {self.db_name}')
            return self.conn
        except sqlite3.Error as err:
            pretty_print('Database does not exist')
            pretty_print(err)

    def close_connection(self)-> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None