import sqlite3

from verifyDB import verifyDB

database = "src\sql\database.db"

conn = sqlite3.connect(database)
cursor = conn.cursor()

if __name__ == "__main__":
    verifyDB(conn)

