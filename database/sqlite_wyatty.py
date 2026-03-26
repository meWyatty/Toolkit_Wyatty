import sqlite3

class MyDatabase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_data(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

# Пример использования:
db = MyDatabase("my_app.db")
db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")
db.execute_query("INSERT INTO users (name, age) VALUES (?, ?)", ("Иван", 25))

users = db.fetch_data("SELECT * FROM users")
print(users)

db.close()