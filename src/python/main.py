import sqlite3
import os
import sys

from verifyDB import verifyDB
from verifyScenes import verifyScenes

database = os.path.join("src", "sql", "database.db")

conn = sqlite3.connect(database)
cursor = conn.cursor()

def main():
    if len(sys.argv) > 1:
        print(sys.argv[1])
        if sys.argv[1] == "verify":
            verifyDB(conn)
            verifyScenes(conn)
            conn.commit()
            conn.close()
        else:
            print("Invalid arguments")
    else:
        print("No arguments was given. Please provide an argument.")
        print("The following arguments are available:")
        print(" - verify: Verify the database and populate it with some data.")
if __name__ == "__main__":
    main()
