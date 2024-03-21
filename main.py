import sqlite3
import os
import re

from src.python.verifyTeaterstykker import verifyTeaterstykkene
from src.python.verifyDB import verifyDB
from src.python.verifyScenes import verifyScenes
from src.python.verifyMedvirkende import verifyMedvirkendeAndStatus
from src.python.verifyTickets import verifyTickets

from src.python.seatPurchase import getFreeSeats, makeCustomerProfile, purchaseTickets
from src.python.models import Skuespiller, Teaterstykket, Akt, Visning, Billett

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
            print(" - makeCustomerProfile <name>, <phone number>, <address>  --> Make a new customer profile.")
            print(" - getFreeSeats <name of play>, <date>  --> Get the number of free seats in each row.")
            print(" - purchaseTickets <name of play>, <date>, <row>, <area>, <amount>, <customer name>, <ticket type>  --> Purchase an amount of tickets on a row.")
            print(" - getPlaysByDate <yyyy-mm-dd>  --> Get all plays on a given date.")
        elif inp == 'verify':
            verifyDB(conn)
            verifyScenes(conn)
            verifyTeaterstykkene(conn)
            verifyMedvirkendeAndStatus(conn)
            verifyTickets(conn)
            conn.commit()
        elif inp.split(' ')[0] == 'getActorsByPlay': 
            play = Teaterstykket.get_by_name(cursor, inp.split(' ')[1])
            if not play:
                print('Play does not exist.')
                continue
            actors = Skuespiller.get_all_by_play(cursor, play.id)
            for actor in actors: 
                print(actor)
        if inp.split(' ')[0] == 'getActorConnections':
            acts = Akt.get_acts_by_actor(cursor, inp.split(' ', 1)[1])
            for act in acts:
                connection = Skuespiller.get_actors_by_act(cursor, act.id)
                for actor in connection:
                    if inp.split(' ', 1)[1] in actor:
                        None
                    else: print(f'Skuespiller_1={inp.split(" ", 1)[1]} ' + actor)

        elif inp.split(' ')[0] == 'getPlaysOnDate':
            plays = Teaterstykket.get_plays_on_date(cursor, inp.split(' ')[1])
            if not plays:
                print('No plays on given date. Date format should be yyyy-mm-dd.')
                continue
            for play in plays:
                count = Billett.get_amount_by_play_and_date(cursor, play.id, inp.split(' ')[1])
                print(play, f'(Solgte_billetter={count})')
        if inp.split(' ')[0] == 'getBestsellingScreening':
            best_play = Visning.get_bestselling(cursor)
            print("Best selling screening is: ", best_play[0].teaterstykket.navn, " at ", best_play[0].dato, ".")
            print("And it has sold: ", best_play[1], " tickets.")
        if inp.split(' ')[0] == 'makeCustomerProfile':
            inp = inp[inp.find(' ')+1:]
            argumentList = [element.strip() for element in inp.split(',')]
            if len(argumentList) != 3:
                print("Invalid number of arguments")
            else:
                makeCustomerProfile(cursor, *argumentList)
                conn.commit()
        if inp.split(' ')[0] == 'getFreeSeats':
            inp = inp[inp.find(' ')+1:]
            argumentList = [element.strip() for element in inp.split(',')]
            if len(argumentList) != 2:
                print("Invalid number of arguments")
            else:
                getFreeSeats(cursor, *argumentList)
        if inp.split(' ')[0] == 'purchaseTickets':
            inp = inp[inp.find(' ')+1:]
            argumentList = [element.strip() for element in inp.split(',')]
            if len(argumentList) != 7:
                print("Invalid number of arguments")
            else:
                purchaseTickets(cursor, *argumentList)
                conn.commit()

    conn.close()
if __name__ == "__main__":
    main()
