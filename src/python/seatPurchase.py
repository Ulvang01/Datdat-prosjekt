from typing import List

import datetime
import sqlite3
import re
from src.python.models import CustomerProfile, TicketPurchase, Ticket, Screening, Chair, TicketPrice, Play


def isValidDate(date: str) -> bool:
    if not re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
        print('Invalid date format, dates must be in format yyyy-mm-dd. eks. 2024-03-20')
        return False
    return True

def isValidPlay(cursor: sqlite3.Cursor, play: str) -> bool:
    if Play.get_by_name(cursor, play) == None:
        print("No play of that name")
        return False
    return True

def isPlayOnDate(cursor: sqlite3.Cursor, date: datetime.date, play: str) -> bool:
    if len(cursor.execute('''SELECT * FROM Screening WHERE date = ? AND play = (
                                    SELECT id FROM Play WHERE name = ?
                                )''', (date, play)).fetchall()) == 0:
        print("No screenings of that play on that day")
        return False
    return True

def isValidArea(cursor: sqlite3.Cursor, play: str, area: str) -> bool:
    validAreas = cursor.execute('''
                    SELECT Area.name FROM Scene JOIN Play ON Scene.name = Play.scene
                        JOIN Area ON Scene.name = Area.Scene 
                            WHERE Play.name = ?
                    ''', (play,)).fetchall()
    validAreas = [element[0] for element in validAreas]
    if not area in validAreas:
        print("No area of that name for that play")
        return False
    return True

def isValidRow(cursor: sqlite3.Cursor, area: str, row: str, play: str) -> bool:
    validRows = cursor.execute('''
                                SELECT Row.row_num FROM Row JOIN Area ON Row.area = Area.id
                                    WHERE Area.id IN (SELECT Area.id FROM Scene 
                                        JOIN Play ON Scene.name = Play.scene
                                            JOIN Area ON Scene.name = Area.Scene 
                                                WHERE Play.name = ?) 
                                        AND Area.name = ?
                                ''', (play, area)).fetchall()
    validRows = [element[0] for element in validRows]
    if not int(row) in validRows:
        print("That row does not exist within the specified area")
        return False
    return True

def isValidCustomer(cursor: sqlite3.Cursor, customer: str) -> bool:
    customer = cursor.execute('SELECT * FROM CustomerProfile WHERE name = ?', (customer,)).fetchall()
    if len(customer) == 0:
        print("There is no customer of that name")
        return False
    return True

def isValidTicketType(cursor: sqlite3.Cursor, ticketType: str, play: str):
    validTicketTypes = cursor.execute('''
                                        SELECT TicketPrice.ticket_type FROM TicketPrice
                                            JOIN Play ON TicketPrice.play = Play.id
                                            WHERE Play.name = ? 
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
    print(date)
    if not isValidPlay(cursor, nameOfPlay):
        return
    if not isPlayOnDate(cursor, date, nameOfPlay):
        return
    
    query = '''
    SELECT Row.id, COUNT(Chair.id) FROM Chair JOIN Ticket ON Chair.id = Ticket.chair 
        RIGHT OUTER JOIN Row ON Chair.row = Row.id
            JOIN Screening ON Ticket.screening = Screening.id 
                JOIN Play ON Screening.play = Play.id
                    WHERE Screening.date = ? AND Play.name = ?
        GROUP BY Row.id
    '''
    tickets = cursor.execute(query, (date, nameOfPlay)).fetchall()
    
    
    query = '''
    SELECT Row.id, Row.row_num, Area.name, COUNT(Chair.id) FROM Row JOIN Area ON Row.area = Area.id
        JOIN Chair ON Chair.row = Row.id
            WHERE Area.scene IN (SELECT Play.scene FROM Play
                WHERE Play.name = ?)
        GROUP BY Row.id
        ORDER BY Area.name, Row.row_num DESC
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
    
    time = cursor.execute("SELECT Play.time FROM Play WHERE name = ?", (play,)).fetchone()[0]
    customerProfile = cursor.execute("SELECT id FROM CustomerProfile WHERE name = ?", (customer,)).fetchone()[0]
    customerProfile = CustomerProfile.get_by_id(cursor, customerProfile)
    
    purchase = TicketPurchase(None, time, date, customerProfile)
    purchase.insert(cursor)
    
    purchaseid = cursor.execute('''
                                SELECT id FROM TicketPurchase 
                                    WHERE customer = ? 
                                        AND date = ?
                                        AND time = ?
                                ''', (customerProfile.id, date, time)).fetchone()[0]
    
    screeningid = cursor.execute('''
                                    SELECT Screening.id FROM Screening JOIN Play ON Screening.play = Play.id
                                        WHERE Screening.date = ? AND Play.name = ?
                                ''', (date, play)).fetchone()[0]
    
    priceid = cursor.execute('''
                                SELECT TicketPrice.id FROM TicketPrice
                                    JOIN Play ON TicketPrice.play = Play.id
                                    WHERE TicketPrice.ticket_type = ? AND Play.name = ?
                             ''', (ticketType, play)).fetchone()[0]
    
    
    
    seatsOnRow = cursor.execute('''
                                SELECT Chair.id FROM Chair 
                                    JOIN Row ON Chair.row = Row.id
                                    JOIN Area ON Row.area = Area.id
                                    JOIN Scene ON Area.scene = Scene.name
                                    JOIN Play ON Play.scene = Scene.name
                                    WHERE Row.row_num = ? 
                                        AND Area.name = ? 
                                        AND Play.name = ?
                                EXCEPT
                                SELECT Chair.id FROM Chair 
                                    JOIN Ticket ON Chair.id = Ticket.Chair
                                ''', (row, area, play)).fetchall()
    
    screening = Screening.get_by_id(cursor, screeningid)
    price = TicketPrice.get_by_id(cursor, priceid)
    purchase = TicketPurchase.get_by_id(cursor, purchaseid)
    
    tickets = []
    for i in range(amount):
        tickets.append(Ticket(None, screening, Chair.get_by_id(cursor, seatsOnRow[i][0]), price, purchase))
    Ticket.upsert_batch(cursor, tickets)
    
    priceForOne = price.price
    print(f"Price: {len(tickets)*priceForOne}")

def makeCustomerProfile(cursor: sqlite3.Cursor, name: str, phoneNr: str, address: str) -> None:
    if not re.fullmatch("[0-9]+", phoneNr):
        print("Invalid phone number, phone number must be a number")
        return
    customer = CustomerProfile(None, name, address, phoneNr)
    try:
        customer.insert(cursor)
    except sqlite3.IntegrityError:
        print("That user already exists")
    else:
        print(f"Customer by name {name} added to database")
