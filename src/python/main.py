import sqlite3
import os

from verifyDB import verifyDB
from populateDB import populateDB

database = os.path.join("src", "sql", "database.db")

conn = sqlite3.connect(database)
cursor = conn.cursor()

if __name__ == "__main__":
    verifyDB(conn)
    populateDB(conn)
