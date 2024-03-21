from typing import List

import datetime
import sqlite3

def concatinateStingList(stringList: List[str]) -> str:
    string = ''
    for element in stringList: string += element.strip() + ' '
    string = string [:-1]
    return string

def getFreeSeats(cursor: sqlite3.Cursor, play: List[str], date: str) -> None:
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:]))
    nameOfPlay = concatinateStingList(play)
    
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
    
    prevArea = ""
    for row in rows:
        if row[2] != prevArea:
            print(row[2])
            prevArea = row[2]
        
        ticketsTaken = 0
        for ticket in tickets:
            if ticket[0] == row[0]:
                ticketsTaken = ticket[1]
                break
        freeSeats = row[3] - ticketsTaken
        print(f"Row: {row[1]} Free Seats: {freeSeats}")
