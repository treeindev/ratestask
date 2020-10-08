import psycopg2
import os

class Database:
    def __init__(self):
        self.host=os.getenv("DATABASE_HOST")
        self.name=os.getenv("DATABASE_NAME")
        self.user=os.getenv("DATABASE_USER")
        self.password=os.getenv("DATABASE_PASSWORD")
        self.connection=None
        self.cursor=None
    
    def connect(self):
        self.connection = psycopg2.connect(
            f"dbname={self.name} user={self.user} host={self.host} password={self.password}"
        )
        self.cursor=self.connection.cursor()
    
    def query(self, query, params=()):
        if not self.cursor:
            raise RuntimeError("Database has not been connected.")

        self.cursor.execute(query, params)
        return self.cursor

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()