import sqlite3
import os

from src.python.verifyTeaterstykker import verifyTeaterstykkene
from src.python.verifyDB import verifyDB
from src.python.verifyScenes import verifyScenes
from src.python.models import Skuespiller, Teaterstykket

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
            print(" - verify  --> Verify the database and populate it with some data.")
            print(" - getActorsByPlay <name of play>  --> Get all actors in a given play.")
        if inp == 'verify':
            verifyDB(conn)
            verifyScenes(conn)
            verifyTeaterstykkene(conn)
            conn.commit()
        if inp.split(' ')[0] == 'getActorsByPlay': 
            play = Teaterstykket.get_by_name(cursor, inp.split(' ')[1])
            if not play:
                print('Play does not exist.')
                continue
            actors = Skuespiller.get_all_by_play(cursor, play.id)
            for actor in actors: 
                print(actor.__str__())
    
    conn.close()
if __name__ == "__main__":
    main()
