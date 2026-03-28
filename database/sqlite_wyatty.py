import sqlite3

class DatabaseSqlite3:
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