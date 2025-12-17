import psycopg2

class PostgresDB:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(self.connection_string)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str):
        if not self.connection:
            raise Exception("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results