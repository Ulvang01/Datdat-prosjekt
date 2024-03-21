import re
import os
import sqlite3
import datetime

from src.python.models import BillettPris, Teaterstykket, Visning, Sal, Rad, Stol, BillettKjøp, KundeProfil, Område, Billett

avspillingPath = os.path.join("src", "res", "avspillingsdager.txt")
kongsemnenePirsPath = os.path.join("src", "res", "priser-Kongsemnene.txt")

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")


def getPris(cursor: sqlite3.Cursor, stykke: Teaterstykket):
    id = cursor.execute("SELECT id FROM BillettPris WHERE teaterstykket = ? AND billett_type = ?", (stykke.id,"Ordinær")).fetchone()[0]
    return BillettPris.get_by_id(cursor, id)

def getVisning(cursor: sqlite3.Cursor, date: str, stykke: Teaterstykket):
    date = map(int, date[5:].split('-'))
    date = datetime.date(*date)
    return Visning.get_by_dato_and_teaterstykke(cursor, date, stykke)

def getStykkeBySal(cursor: sqlite3.Cursor, sal: Sal):
    id = cursor.execute("SELECT id FROM Teaterstykket WHERE sal = ?", (sal.navn,)).fetchone()[0]
    return Teaterstykket.get_by_id(cursor, id)

def getStol(cursor: sqlite3.Cursor, stolnr: str, rad: Rad):
    id = cursor.execute("SELECT id FROM Stol WHERE stol_nr = ? AND rad = ?", (stolnr, rad.id)).fetchone()[0]
    return Stol.get_by_id(cursor, id)

def getKjøp(cursor: sqlite3.Cursor, tid: str, dato: datetime.date, user: KundeProfil):
    id = cursor.execute("SELECT id FROM BillettKjøp WHERE tid = ? AND dato = ? AND kunde = ?", (tid, dato, user.id)).fetchone()[0]
    return BillettKjøp.get_by_id(cursor, id)



def verifyUser(cursor: sqlite3.Cursor) -> int:
    defaultName = "default"
    userAlreadyExists = cursor.execute("SELECT id FROM Kundeprofil WHERE navn = ?", (defaultName,)).fetchall()
    
    if not userAlreadyExists:
        defaultUser = KundeProfil(None, defaultName, "", "")
        defaultUser.insert(cursor)
    
    # return user
    userid = cursor.execute("SELECT id FROM Kundeprofil WHERE navn = ?", (defaultName,)).fetchone()[0] 
    return KundeProfil.get_by_id(cursor, userid)

def verification(cursor: sqlite3.Cursor, salnavn: str, user: KundeProfil, sceneLines: list['str']):
    sal = Sal.get_by_name(cursor, salnavn)
    stykke = getStykkeBySal(cursor, sal)
    pris = getPris(cursor, stykke)
    visning = getVisning(cursor, sceneLines[-1], stykke)
    
    kjøp = BillettKjøp(None, stykke.tid, visning.dato, user)
    kjøp.insert(cursor)
    kjøp = getKjøp(cursor, kjøp.time, kjøp.dato, kjøp.kundeProfile)

    areas = Område.get_by_sal(cursor, sal)
    sortedAreas = []
    for line in sceneLines:
        if not re.match(r"\d", line):
            for area in areas:
                if line.strip() == area.navn:
                    sortedAreas.append(area)
    areas = sortedAreas

    return {
        'sal': sal,
        'visning': visning,
        'pris': pris,
        'kjøp': kjøp,
        'areas': areas,
    }

def verifyHovedscenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
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
                radid = cursor.execute("SELECT id FROM Rad WHERE område = ? AND radnr = ?", (result['areas'][areaIndex].id, rowNr)).fetchone()[0]
                rad = Rad(radid, rowNr, result['areas'][areaIndex])
                
                stol = getStol(cursor, (charIndex+1)+(rowNr - 1)*len(hovedsceneLines[rowNr - 1]), rad)

                ticket = Billett(None, result['visning'], stol, result['pris'], result['kjøp'])
                tickets.append(ticket)
    
    Billett.upsert_batch(cursor, tickets)

def verifyGamlescenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
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
                radid = cursor.execute("SELECT id FROM Rad WHERE område = ? AND radnr = ?", (result['areas'][areaIndex].id, rowNr)).fetchone()[0]
                rad = Rad(radid, rowNr, result['areas'][areaIndex])
                stol = getStol(cursor, charIndex+1, rad)
                ticket = Billett(None, result['visning'], stol, result['pris'], result['kjøp'])
                tickets.append(ticket)
    Billett.upsert_batch(cursor, tickets)


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