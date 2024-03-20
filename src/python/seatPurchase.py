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
    print(play, type(date))
    nameOfPlay = concatinateStingList(play)
    print(nameOfPlay)
    
    query = '''
    SELECT Stol.rad, COUNT(Stol.id) FROM Stol JOIN Billett ON Stol.id = Billett.stol 
	    JOIN Visning ON Billett.visning = Visning.id 
            JOIN Teaterstykket ON Visning.teaterstykket = Teaterstykket.id
		        WHERE Visning.dato = ? AND Teaterstykket.navn = ?
        GROUP BY Stol.rad
    '''
    tickets = cursor.execute(query, (date, nameOfPlay)).fetchall()
    print(tickets)
    print(len(tickets))
    
    query = '''
    SELECT Rad.id, Rad.radnr, Område.navn FROM Rad JOIN Område ON Rad.område = Område.id
        WHERE Område.sal IN (SELECT Teaterstykket.sal FROM Teaterstykket
            WHERE Teaterstykket.navn = ?)
    '''
    rows = cursor.execute(query, (nameOfPlay,)).fetchall()
    print(rows)