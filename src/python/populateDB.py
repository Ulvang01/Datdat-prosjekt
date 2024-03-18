from models import Sal, Område, Rad, Stol
import re

def populateHovedsal(cursor):
    hovedscene = Sal("hovedscene")
    cursor.execute(hovedscene.get())
    if cursor.fetchone() is None:
        cursor.execute(hovedscene.insert())

    with open('FilesNeeded/hovedscenen.txt', 'r') as file:
        content = file.readlines()

    content = content[1:]
    current_område = None
    område_counter = 0
    rad_counter = 0
    stol_counter = 0

    all_områder_db = cursor.execute(Område.get_all()).fetchall()
    all_rad_db = cursor.execute(Rad.get_all()).fetchall()
    all_stol_db = cursor.execute(Stol.get_all()).fetchall()

    all_områder = []
    print("Getting all områder")
    for område in all_områder_db:
        gameltOmråde = Område(område[0], område[1], område[2])
        all_områder.append(gameltOmråde)

    for område in all_områder:
        print(område.__str__())

    for row in content:
        hasDigit = bool(re.search(r'\d', row))
        if not hasDigit and row.strip() != "":
            current_område = Område(område_counter, row.strip(), hovedscene)
            exist = False
            for område in all_områder:
                if current_område.navn == område.navn and current_område.sal.navn == område.sal and current_område.id == område.id:
                    current_område = område
                    exist = True
                    break
            if not exist:
                print(current_område.insert())
                cursor.execute(current_område.insert())
                all_områder.append(current_område)
            område_counter += 1

    content = content[::-1]
    område_counter = 0
    current_område = all_områder[område_counter]
    all_rad = []
    print("Getting all rad")
    for rad in all_rad_db:
        gamelRad = Rad(rad[0], rad[1], rad[2])
        all_rad.append(gamelRad)
    
    all_stol = []
    print("Getting all stol")
    for stol in all_stol_db:
        gamelStol = Stol(stol[0], stol[1], stol[2])
        all_stol.append(gamelStol)

    for row in content:
        row = row.strip()
        print("Row: ", rad_counter)
        hasDigit = bool(re.search(r'\d', row))
        print("Has digit: ", hasDigit)
        if not hasDigit and row.strip() != "":
            current_område = all_områder[område_counter]
            område_counter += 1
        elif hasDigit and row.strip() != "":
            current_rad = Rad(rad_counter, rad_counter + 1, current_område.navn)
            if current_rad not in all_rad:
                print(current_rad.insert())
                cursor.execute(current_rad.insert())
                all_rad.append(current_rad)
            rad_counter += 1
            for i in range(1, len(row.strip()) + 1):
                print(i)
                if row[i - 1] == "x":
                    stol_counter += 1
                    continue
                current_stol = Stol(stol_counter, stol_counter + 1, current_rad)
                if current_stol not in all_stol:
                    print(current_stol.insert())
                    cursor.execute(current_stol.insert())
                    all_stol.append(current_stol)
                stol_counter += 1


def populateDB(conn):
    '''Populate the database with some data'''
    cursor = conn.cursor()
    populateHovedsal(cursor)
    conn.commit()