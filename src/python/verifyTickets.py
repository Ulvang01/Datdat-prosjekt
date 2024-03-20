import re
import os
import sqlite3
import datetime

from models import * # TODO: only the models I need

avspillingPath = os.path.join("src", "res", "avspillingsdager.txt")
kongsemnenePirsPath = os.path.join("src", "res", "priser-Kongsemnene.txt")

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")

def getVisning(cursor: sqlite3.Cursor, date: str, stykke: Teaterstykket):
    date = map(int, date[5:].split('-'))
    date = datetime.date(*date)
    return Visning.get_by_dato_and_teaterstykke(cursor, date, stykke)

def getStykkeBySal(cursor: sqlite3.Cursor, sal: Sal):
    id = cursor.execute("SELECT id FROM Teaterstykket WHERE sal = ?", (sal.navn,)).fetchone()[0]
    return Teaterstykket.get_by_id(cursor, id)


def verifyUser(cursor: sqlite3.Cursor) -> int:
    defaultName = "default"
    userAlreadyExists = cursor.execute("SELECT id FROM Kundeprofil WHERE navn = ?", (defaultName,)).fetchall()
    
    if not userAlreadyExists:
        defaultUser = KundeProfil(None, defaultName, "", "")
        defaultUser.insert(cursor)
    
    # return user
    userid = cursor.execute("SELECT id FROM Kundeprofil WHERE navn = ?", (defaultName,)).fetchone()[0] 
    return KundeProfil.get_by_id(cursor, userid)

def verifyHovedscenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
    with open(hovedScenePath, 'r') as hovedscene:
        hovedsceneLines = hovedscene.readlines()
        hovedscene.close()
    
    hovedsceneLines = hovedsceneLines[::-1]
    
    sal = Sal.get_by_name(cursor, "Hovedscene")
    stykke = getStykkeBySal(cursor, sal)
    
    visning = getVisning(cursor, hovedsceneLines[-1], stykke)
    
    hovedsceneKjøp = BillettKjøp(None, stykke.tid, visning.dato, user)
    hovedsceneKjøp.insert(cursor)
    print(hovedsceneKjøp)
    
    areas = Område.get_by_sal(cursor, sal)
    areaName = ""
    for line in hovedsceneLines:
        if not re.match("\d", line):
            areaName = line.strip()
            break
    
    area = None
    for element in areas:
        if element.navn == areaName:
            area = element
    
    print(hovedsceneLines)
    
    for lineIndex in range(len(hovedsceneLines)):
        if not re.match("\d", hovedsceneLines[lineIndex]):
            break
        
        print("raden:", lineIndex+1)
        
        for charIndex in range(len(hovedsceneLines[lineIndex])):
            if hovedsceneLines[lineIndex][charIndex] == '1':
                radid = cursor.execute("SELECT id FROM Rad WHERE område = ? AND radnr = ?", (area.id, lineIndex+1)).fetchone()[0]
                print(radid)
                rad = Rad(radid, lineIndex+1, area)
                print("radnr", lineIndex+1)
                print(cursor.execute("SELECT * FROM Stol WHERE rad = ?", (rad.id,)).fetchall())
                #stol = Stol(None, (charIndex+1)*(lineIndex+1), )
                #ticket = Billett(None, visning, stol, billettPris, hovedsceneKjøp)

def verifyGamlescenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
    pass

def verifyTickets(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    user = verifyUser(cursor)
    print(user)
    verifyHovedscenePurchase(cursor, user)
    verifyGamlescenePurchase(cursor, user)
    conn.commit()

if __name__ == "__main__":
    database = os.path.join("src", "sql", "database.db")
    conn = sqlite3.connect(database)
    verifyTickets(conn)