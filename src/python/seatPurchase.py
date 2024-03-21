from typing import List

import datetime
import sqlite3
import re
from src.python.models import KundeProfil, BillettKjøp, Billett, Visning, Stol, BillettPris


def isValidDate(date: str) -> bool:
    if not re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
        print('Invalid date format, dates must be in format yyyy-mm-dd. eks. 2024-03-20')
        return False
    return True

def isValidPlay(cursor: sqlite3.Cursor, play: str) -> bool:
    if len(cursor.execute("SELECT * FROM Teaterstykket WHERE navn = ?", (play,)).fetchall()) == 0:
        print("No play of that name")
        return False
    return True

def isPlayOnDate(cursor: sqlite3.Cursor, date: datetime.date, play: str) -> bool:
    if len(cursor.execute('''SELECT * FROM Visning WHERE dato = ? AND teaterstykket = (
                                    SELECT id FROM Teaterstykket WHERE navn = ?
                                )''', (date, play)).fetchall()) == 0:
        print("No screenings of that play on that day")
        return False
    return True

def isValidArea(cursor: sqlite3.Cursor, play: str, area: str) -> bool:
    validAreas = cursor.execute('''
                    SELECT Område.navn FROM Sal JOIN Teaterstykket ON Sal.navn = Teaterstykket.sal
                        JOIN Område ON Sal.navn = Område.Sal 
                            WHERE Teaterstykket.navn = ?
                    ''', (play,)).fetchall()
    validAreas = [element[0] for element in validAreas]
    if not area in validAreas:
        print("No area of that name for that play")
        return False
    return True

def isValidRow(cursor: sqlite3.Cursor, area: str, row: str, play: str) -> bool:
    validRows = cursor.execute('''
                                SELECT Rad.radnr FROM Rad JOIN Område ON Rad.område = Område.id
                                    WHERE Område.id IN (SELECT Område.id FROM Sal 
                                        JOIN Teaterstykket ON Sal.navn = Teaterstykket.sal
                                            JOIN Område ON Sal.navn = Område.Sal 
                                                WHERE Teaterstykket.navn = ?) 
                                        AND Område.navn = ?
                                ''', (play, area)).fetchall()
    validRows = [element[0] for element in validRows]
    if not int(row) in validRows:
        print("That row does not exist within the specified area")
        return False
    return True

def isValidCustomer(cursor: sqlite3.Cursor, customer: str) -> bool:
    customer = cursor.execute('SELECT * FROM Kundeprofil WHERE navn = ?', (customer,)).fetchall()
    if len(customer) == 0:
        print("There is no customer of that name")
        return False
    return True

def isValidTicketType(cursor: sqlite3.Cursor, ticketType: str, play: str):
    validTicketTypes = cursor.execute('''
                                        SELECT BillettPris.billett_type FROM BillettPris
                                            JOIN Teaterstykket ON BillettPris.teaterstykket = Teaterstykket.id
                                            WHERE Teaterstykket.navn = ? 
                                      ''', (play,)).fetchall()
    validTicketTypes = [element[0] for element in validTicketTypes]
    if not ticketType in validTicketTypes:
        print("No ticket type of that name found for that play")
        return False
    return True


def getFreeSeats(cursor: sqlite3.Cursor, nameOfPlay: str, date: str, shouldPrint: bool = True) -> None:
    if not isValidDate(date):
        return
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:]))
    
    if not isValidPlay(cursor, nameOfPlay):
        return
    if not isPlayOnDate(cursor, date, nameOfPlay):
        return
    
    query = '''
    SELECT Rad.id, COUNT(Stol.id) FROM Stol JOIN Billett ON Stol.id = Billett.stol 
        RIGHT OUTER JOIN Rad ON Stol.rad = Rad.id
            JOIN Visning ON Billett.visning = Visning.id 
                JOIN Teaterstykket ON Visning.teaterstykket = Teaterstykket.id
                    WHERE Visning.dato = ? AND Teaterstykket.navn = ?
        GROUP BY Rad.id
    '''
    tickets = cursor.execute(query, (date, nameOfPlay)).fetchall()
    
    
    query = '''
    SELECT Rad.id, Rad.radnr, Område.navn, COUNT(Stol.id) FROM Rad JOIN Område ON Rad.område = Område.id
        JOIN Stol ON Stol.rad = Rad.id
            WHERE Område.sal IN (SELECT Teaterstykket.sal FROM Teaterstykket
                WHERE Teaterstykket.navn = ?)
        GROUP BY Rad.id
        ORDER BY Område.navn, Rad.radnr DESC
    '''
    rows = cursor.execute(query, (nameOfPlay,)).fetchall()
    
    rowAndAvailableSeats = []
    
    prevArea = ""
    for row in rows:
        if row[2] != prevArea:
            if shouldPrint: print(row[2])
            prevArea = row[2]
        
        ticketsTaken = 0
        for ticket in tickets:
            if ticket[0] == row[0]:
                ticketsTaken = ticket[1]
                break
        freeSeats = row[3] - ticketsTaken
        if shouldPrint: print(f"Row: {row[1]} Free Seats: {freeSeats}")
        rowAndAvailableSeats.append((row[0], freeSeats))
    
    return rowAndAvailableSeats

def purchaseTickets(cursor: sqlite3.Cursor, play: str, date: str, row: str, area: str, amount: str, customer: str, ticketType: str):
    if not isValidDate(date):
        return
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:]))
    
    if not isValidPlay(cursor, play):
        return
    if not isPlayOnDate(cursor, date, play):
        return
    
    if not isValidArea(cursor, play, area):
        return
    
    if not isValidRow(cursor, area, row, play):
        return
    
    try:
        amount = int(amount)
    except:
        print("Amount must be a number")
        return
    
    freeSeats = getFreeSeats(cursor, play, str(date), False)
    if freeSeats is None:
        print("Internal error")
        return
    
    for element in freeSeats:
        if element[0] == int(row):
            if amount > element[1]:
                print("Amount is too large for the amount of seats available on that row")
                return 
            break
    
    if not isValidCustomer(cursor, customer):
        return
    
    if not isValidTicketType(cursor, ticketType, play):
        return
    
    time = cursor.execute("SELECT Teaterstykket.tid FROM Teaterstykket WHERE navn = ?", (play,)).fetchone()[0]
    customerProfile = cursor.execute("SELECT id FROM Kundeprofil WHERE navn = ?", (customer,)).fetchone()[0]
    customerProfile = KundeProfil.get_by_id(cursor, customerProfile)
    
    purchase = BillettKjøp(None, time, date, customerProfile)
    purchase.insert(cursor)
    
    purchaseid = cursor.execute('''
                                SELECT id FROM BillettKjøp 
                                    WHERE kunde = ? 
                                        AND dato = ?
                                        AND tid = ?
                                ''', (customerProfile.id, date, time)).fetchone()[0]
    
    screeningid = cursor.execute('''
                                    SELECT Visning.id FROM Visning JOIN Teaterstykket ON Visning.teaterstykket = Teaterstykket.id
                                        WHERE Visning.dato = ? AND Teaterstykket.navn = ?
                                ''', (date, play)).fetchone()[0]
    
    priceid = cursor.execute('''
                                SELECT BillettPris.id FROM BillettPris
                                    JOIN Teaterstykket ON BillettPris.teaterstykket = Teaterstykket.id
                                    WHERE BillettPris.billett_type = ? AND Teaterstykket.navn = ?
                             ''', (ticketType, play)).fetchone()[0]
    
    
    
    seatsOnRow = cursor.execute('''
                                SELECT Stol.id FROM Stol 
                                    JOIN Rad ON Stol.rad = Rad.id
                                    JOIN Område ON Rad.område = Område.id
                                    JOIN Sal ON Område.sal = Sal.navn
                                    JOIN Teaterstykket ON Teaterstykket.sal = Sal.navn
                                    WHERE Rad.radnr = ? 
                                        AND Område.navn = ? 
                                        AND Teaterstykket.navn = ?
                                EXCEPT
                                SELECT Stol.id FROM Stol 
                                    JOIN Billett ON Stol.id = Billett.Stol
                                ''', (row, area, play)).fetchall()
    
    screening = Visning.get_by_id(cursor, screeningid)
    price = BillettPris.get_by_id(cursor, priceid)
    purchase = BillettKjøp.get_by_id(cursor, purchaseid)
    
    tickets = []
    for i in range(amount):
        tickets.append(Billett(None, screening, Stol.get_by_id(cursor, seatsOnRow[i][0]), price, purchase))
    Billett.upsert_batch(cursor, tickets)
    
    priceForOne = price.pris
    print(f"Price: {len(tickets)*priceForOne}")

def makeCustomerProfile(cursor: sqlite3.Cursor, name: str, phoneNr: str, address: str) -> None:
    if not re.fullmatch("[0-9]+", phoneNr):
        print("Invalid phone number, phone number must be a number")
        return
    customer = KundeProfil(None, name, address, phoneNr)
    try:
        customer.insert(cursor)
    except sqlite3.IntegrityError:
        print("That user already exists")
    else:
        print(f"Customer by name {name} added to database")
