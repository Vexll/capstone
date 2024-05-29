import sqlite3


class Database:
    @staticmethod
    def connection():
        sqlite_connection = None
        filename = 'capstone.db'
        try:
            sqlite_connection = sqlite3.connect(filename)
            print("Connected to SQLite")
        except sqlite3.Error as error:
            print("Failed to connect with sqlite3 DB", error)
        return sqlite_connection
