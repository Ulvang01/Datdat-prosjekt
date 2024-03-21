import re
import os
import sqlite3
import datetime

from src.python.models import TicketPrice, Play, Screening, Scene, Row, Chair, TicketPurchase, CustomerProfile, Area, Ticket

screeningPath = os.path.join("src", "res", "screening-dates.txt")

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")

def getVisning(cursor: sqlite3.Cursor, date: str, play: Play):
    date = map(int, date[5:].split('-'))
    date = datetime.date(*date)
    return Screening.get_by_date_and_play(cursor, date, play)

def verifyUser(cursor: sqlite3.Cursor) -> int:
    defaultName = "default"

    defaultUser = CustomerProfile(None, defaultName, "dummyAddress", "")
    defaultUser.insert(cursor)    
    defaultUser = CustomerProfile.get_by_name_and_address(cursor, defaultName, "dummyAddress")
    
    return defaultUser

def verification(cursor: sqlite3.Cursor, scene_name: str, user: CustomerProfile, sceneLines: list['str']):
    scene = Scene.get_by_name(cursor, scene_name)
    play = Play.get_by_scene(cursor, scene)
    price = TicketPrice.get_by_play_and_type(cursor, play, "Ordinær")
    screening = getVisning(cursor, sceneLines[-1], play)
    
    purchase = TicketPurchase(None, play.time, screening.date, user)
    purchase.insert(cursor)
    purchase = TicketPurchase.get_by_time_date_and_customer(cursor, play.time, screening.date, user)

    areas = Area.get_by_scene(cursor, scene)
    sortedAreas = []
    for line in sceneLines:
        if not re.match(r"\d", line):
            for area in areas:
                if line.strip() == area.name:
                    sortedAreas.append(area)
    areas = sortedAreas

    return {
        'scene': scene,
        'screening': screening,
        'price': price,
        'purchase': purchase,
        'areas': areas,
    }

def verifyHovedscenePurchase(cursor: sqlite3.Cursor, user: CustomerProfile) -> None:
    with open(hovedScenePath, 'r') as hovedscene:
        hovedsceneLines = hovedscene.readlines()
        hovedscene.close()
    
    hovedsceneLines = [line.strip() for line in hovedsceneLines[::-1]]
    result = verification(cursor, 'Hovedscene', user, hovedsceneLines)

    tickets = []
    areaIndex = 0
    rowNr = 0
    for line in hovedsceneLines:
        rowNr += 1
        if not re.match(r"\d", line):
            areaIndex += 1
            continue
        
        for charIndex in range(len(line)):
            if line[charIndex] == '1':
                row = Row.get_by_area_and_row_num(cursor, result['areas'][areaIndex], rowNr)
                chair = Chair.get_by_row_and_num(cursor, row, (charIndex+1)+(rowNr - 1)*len(hovedsceneLines[rowNr - 1]))
                ticket = Ticket(None, result['screening'], chair, result['price'], result['purchase'])
                tickets.append(ticket)
    
    Ticket.upsert_batch(cursor, tickets)

def verifyGamlescenePurchase(cursor: sqlite3.Cursor, user: CustomerProfile) -> None:
    with open(gamleScenePath, 'r') as gamlescene:
        gamlesceneLines = gamlescene.readlines()
        gamlescene.close()

    gamlesceneLines = [line.strip() for line in gamlesceneLines[::-1]]
    
    result = verification(cursor, 'Gamle-scene', user, gamlesceneLines)
    
    areaIndex = 0
    rowNr = 0
    tickets = []
    for line in gamlesceneLines:
        rowNr += 1
        if not re.match(r"\d", line):
            areaIndex += 1
            rowNr = 0
            continue
        
        for charIndex in range(len(line)):
            if line[charIndex] == '1':
                row = Row.get_by_area_and_row_num(cursor, result['areas'][areaIndex], rowNr)
                chair = Chair.get_by_row_and_num(cursor, row, charIndex+1)
                ticket = Ticket(None, result['screening'], chair, result['price'], result['purchase'])
                tickets.append(ticket)
    Ticket.upsert_batch(cursor, tickets)


def verifyTickets(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    print("Adding dummy user...")
    user = verifyUser(cursor)
    
    print("Verifying tickets...")
    verifyHovedscenePurchase(cursor, user)
    verifyGamlescenePurchase(cursor, user)
    conn.commit()

if __name__ == "__main__":
    database = os.path.join("src", "sql", "database.db")
    conn = sqlite3.connect(database)
    verifyTickets(conn)