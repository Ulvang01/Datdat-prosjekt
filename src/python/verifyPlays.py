import re
import os

from src.python.models import Scene, Play, Screening, TicketPrice, Act, Actor, Role, ActorRoleJunction, RoleActJunction
from datetime import datetime

screeningPath = os.path.join("src", "res", "screening-dates.txt")

def verifyPlay(name: str, act_num: int, cursor):
    pricesPath = os.path.join('src', 'res', 'prices-' + name.replace(" ", "_") + '.txt')
    contributorsPath = os.path.join('src', 'res', 'actors-' + name.replace(" ", "_") + '.txt')
    rolesPath = os.path.join('src', 'res', 'roles-' + name.replace(" ", "_") + '.txt')

    print("Verifying " + name + "...")
    try:
        with open(screeningPath, 'r') as file:
            content = file.readlines()
            for line in content:
                if name == line.split(", ")[0]:
                    content = line.split(", ")

        scene = Scene.get_by_name(cursor, content[2].strip())
        print(scene,"'" + content[2] + "'")
        play = Play(None, name, content[1], content[3], scene)
        play.insert(cursor)
        play = Play.get_by_name(cursor, name)

        print("Verifying screenings...")
        screening_list = []
        for i in range(4, len(content)):
            full_date = content[i] + " 2024"
            dateobj = datetime.strptime(full_date, "%d.%b %Y")
            sql_date = dateobj.strftime("%Y-%m-%d")
            screening_list.append(Screening(None, sql_date, play))
        
        Screening.upsert_batch(cursor, screening_list)

        print("Verifying ticketprices...")
        with open(pricesPath, 'r') as file:
            content = file.readlines()
        
        ticketprice_list = []
        for i in range(len(content)):
            ticketprice_list.append(TicketPrice(None, content[i].split(": ")[1], content[i].split(": ")[0], play))
        
        TicketPrice.upsert_batch(cursor, ticketprice_list)

        print("Verifying actors...")
        with open(contributorsPath, 'r') as file:
            content = file.readlines()

        for i in range(len(content)):
            navn = content[i].split(" : ")[0]
            rolle = content[i].split(" : ")[1].strip().split(" / ")
            for r in rolle:
                if not Role.get_by_name(cursor, r):
                    roller = Role(None, r)
                    roller.insert(cursor)
                actors = Actor.get_by_name(cursor, navn)
                if not actors:
                    actors = Actor(None, navn)
                    actors.insert(cursor)
                skuespillerRolleJunction = ActorRoleJunction(Actor.get_by_name(cursor, navn), Role.get_by_name(cursor, r))
                skuespillerRolleJunction.insert(cursor)

        print("Verifying acts...")
        with open(rolesPath, 'r') as file:
            content = file.readlines()[1:]

        act_list = []
        for i in range(act_num):
            act_list.append(Act(None, i + 1, play))

        Act.upsert_batch(cursor, act_list)

        for line in content:
            rollenavn = line.split(" : ")[0]
            acts = line.split(" : ")[1].strip().split(", ")
            for a in acts:
                act = Act.get_by_number_and_play(cursor, int(a), play)
                if not act:
                    act = Act(None, int(a), play)
                    act.insert(cursor)
                rolle = Role.get_by_name(cursor, rollenavn)
                if not rolle:
                    rolle = Role(None, rollenavn)
                    rolle.insert(cursor)
                aktRolleJunction = RoleActJunction(act, Role.get_by_name(cursor, rollenavn))
                aktRolleJunction.insert(cursor)

        cursor.execute("COMMIT;")
    except Exception as e:
        print("Error reading " + name + "...")
        print(e.with_traceback(e.__traceback__))
        return
    

def verifyPlays(conn):
    '''Verify the database with the plays'''
    cursor = conn.cursor()
    verifyPlay("Kongsemnene", 5, cursor)
    verifyPlay("Størst av alt er kjærligheten", 1, cursor)
    conn.commit()
    return
