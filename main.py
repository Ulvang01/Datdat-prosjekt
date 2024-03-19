import sqlite3
import os

from src.python.verifyTeaterstykker import verifyTeaterstykkene
from src.python.verifyDB import verifyDB
from src.python.verifyScenes import verifyScenes

database = os.path.join("src", "sql", "database.db")

conn = sqlite3.connect(database)
cursor = conn.cursor()

def main():
    print("To exit program, enter 'x'")
    print("If you need help, type 'help'")
    while True:
        inp = input()
        if inp == 'x':
            break
        if inp == 'help':
            print("\nThe following arguments are available:")
            print(" - verify: Verify the database and populate it with some data.")
        if inp == 'verify':
            verifyDB(conn)
            verifyScenes(conn)
            verifyTeaterstykkene(conn)
            conn.commit()
    
    conn.close()
if __name__ == "__main__":
    main()
