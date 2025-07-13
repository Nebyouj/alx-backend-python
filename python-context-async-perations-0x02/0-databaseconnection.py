import sqlite3

class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Usage
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
