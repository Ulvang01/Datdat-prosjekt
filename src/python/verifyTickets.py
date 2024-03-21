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


def verifyHovedscenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
    with open(hovedScenePath, 'r') as hovedscene:
        hovedsceneLines = hovedscene.readlines()
        hovedscene.close()
    
    hovedsceneLines = [line.strip() for line in hovedsceneLines[::-1]]
    
    sal = Sal.get_by_name(cursor, "Hovedscene")
    stykke = getStykkeBySal(cursor, sal)
    pris = getPris(cursor, stykke)
    
    #print(pris)
    
    visning = getVisning(cursor, hovedsceneLines[-1], stykke)
    
    hovedsceneKjøp = BillettKjøp(None, stykke.tid, visning.dato, user)
    hovedsceneKjøp.insert(cursor)
    hovedsceneKjøp = getKjøp(cursor, hovedsceneKjøp.time, hovedsceneKjøp.dato, hovedsceneKjøp.kundeProfile)
    #print(hovedsceneKjøp)
    
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
            break
    
    tickets = []
    for lineIndex in range(len(hovedsceneLines)):
        if not re.match("\d", hovedsceneLines[lineIndex]):
            break
        
        #print("raden:", lineIndex+1)
        
        for charIndex in range(len(hovedsceneLines[lineIndex])):
            if hovedsceneLines[lineIndex][charIndex] == '1':
                radid = cursor.execute("SELECT id FROM Rad WHERE område = ? AND radnr = ?", (area.id, lineIndex+1)).fetchone()[0]
                rad = Rad(radid, lineIndex+1, area)
                
                stol = getStol(cursor, (charIndex+1)+(lineIndex)*len(hovedsceneLines[lineIndex]), rad)
                #print(stol)
                ticket = Billett(None, visning, stol, pris, hovedsceneKjøp)
                tickets.append(ticket)
    
    Billett.upsert_batch(cursor, tickets)

def verifyGamlescenePurchase(cursor: sqlite3.Cursor, user: KundeProfil) -> None:
    with open(gamleScenePath, 'r') as gamlescene:
        gamlesceneLines = gamlescene.readlines()
        gamlescene.close()
    
    dateLine = gamlesceneLines[0].strip()
    gamlesceneLines = gamlesceneLines[1:]
    gamlesceneLines = gamlesceneLines[::-1]
    sal = Sal.get_by_name(cursor, "Gamle-scene")
    stykke = getStykkeBySal(cursor, sal)
    pris = getPris(cursor, stykke)
    visning = getVisning(cursor, dateLine, stykke)
    
    gamlesceneKjøp = BillettKjøp(None, stykke.tid, visning.dato, user)
    gamlesceneKjøp.insert(cursor)
    gamlesceneKjøp = getKjøp(cursor, gamlesceneKjøp.time, gamlesceneKjøp.dato, gamlesceneKjøp.kundeProfile)
    
    areas = Område.get_by_sal(cursor, sal)
    sortedAreas = []
    print(areas)
    for line in gamlesceneLines:
        if not re.match("\d", line):
            for area in areas:
                if line.strip() == area.navn:
                    sortedAreas.append(area)
    areas = sortedAreas
    
    areaIndex = 0
    rowNr = 0
    tickets = []
    for line in gamlesceneLines:
        rowNr += 1
        if not re.match("\d", line):
            areaIndex += 1
            rowNr = 0
            continue
        
        for charIndex in range(len(line)):
            if line[charIndex] == '1':
                radid = cursor.execute("SELECT id FROM Rad WHERE område = ? AND radnr = ?", (areas[areaIndex].id, rowNr)).fetchone()[0]
                rad = Rad(radid, rowNr, areas[areaIndex])
                stol = getStol(cursor, charIndex+1, rad)
                ticket = Billett(None, visning, stol, pris, gamlesceneKjøp)
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