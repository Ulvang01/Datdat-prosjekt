import sqlite3
import os

from src.python.verifyPlays import verifyPlays
from src.python.verifyDB import verifyDB
from src.python.verifyScenes import verifyScenes
from src.python.verifyContributors import verifyContributorsAndStatus
from src.python.models import Actor, Play, Screening

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
            print(" - getBestsellingScreening  --> Get the best selling screening.")
        if inp == 'verify':
            verifyDB(conn)
            verifyScenes(conn)
            verifyPlays(conn)
            verifyContributorsAndStatus(conn)
            conn.commit()
        if inp.split(' ')[0] == 'getActorsByPlay': 
            play = Play.get_by_name(cursor, inp.split(' ')[1])
            if not play:
                print('Play does not exist.')
                continue
            actors = Actor.get_all_by_play(cursor, play.id)
            for actor in actors: 
                print(actor.__str__())
        if inp.split(' ')[0] == 'getBestsellingScreening':
            best_play = Screening.get_bestselling(cursor)
            print("Best selling screening is: ", best_play[0].teaterstykket.navn, " at ", best_play[0].dato, ".")
            print("And it has sold: ", best_play[1], " tickets.")

    conn.close()
if __name__ == "__main__":
    main()
