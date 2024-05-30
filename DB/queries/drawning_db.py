import sqlite3
from DB.database import Database


# table_creation_query = ("""
#         CREATE TABLE drowning (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         city TEXT,
#         latitude DECIMAL,
#         longitude DECIMAL,
#         datetime TEXT
#         );""")


class DrawningDB:
    @staticmethod
    def add_drawning_case(city: str, latitude: float, longitude: float, datetime: str):
        try:
            conn = Database.connection()
            cursor = conn.cursor()
            query = ("""
                INSERT INTO drowning (city, latitude, longitude, datetime)
                values (?, ?, ?, ?)
            """)
            cursor.execute(query, (city, latitude, longitude, datetime))
            conn.commit()
            print("the case has inserted successfully")
            conn.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)



    @staticmethod
    def view_all_cases():
        try:
            conn = Database.connection()
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM drowning"
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            result = {row['id']: dict(row) for row in rows}
            conn.close()
            return result
        except sqlite3.Error as e:
            print("SQLite error:", e)

