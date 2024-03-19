from models import Sal, Område, Rad, Stol
import re

def verifyHovedscene(cursor):
    '''Verify the database with the hovedsal'''
    print("Verifying hovedscene...")
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
    print(all_stol_db)

    all_områder = []
    print("Getting all områder...")
    for område in all_områder_db:
        gameltOmråde = Område(område[0], område[1], område[2])
        all_områder.append(gameltOmråde)

    print("Verifying områder...")
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
                cursor.execute(current_område.insert())
                all_områder.append(current_område)
            område_counter += 1

    content = content[::-1]
    område_counter = 0
    current_område = all_områder[område_counter]
    all_rad = []
    print("Getting all rad...")
    for rad in all_rad_db:
        for område in all_områder:
            if rad[2] == område.navn:
                gamelRad = Rad(rad[0], rad[1], område)
                all_rad.append(gamelRad)
                break
    
    all_stol = []
    print("Getting all stol...")
    for stol in all_stol_db:
        for rad in all_rad:
            if stol[2] == rad.id:
                gamelStol = Stol(stol[0], stol[1], rad)
                all_stol.append(gamelStol)
                print(gamelStol)
                break
    
    print("Verifying rad and stol...")
    for row in content:
        row = row.strip()
        hasDigit = bool(re.search(r'\d', row))
        if not hasDigit and row.strip() != "":
            current_område = all_områder[område_counter]
            område_counter += 1
        elif hasDigit and row.strip() != "":
            current_rad = Rad(rad_counter, rad_counter + 1, current_område)
            exist = False
            for rad in all_rad:
                if current_rad.radnr == rad.radnr and current_rad.område.navn == rad.område.navn and current_rad.id == rad.id:
                    current_rad = rad
                    exist = True
                    break
            if not exist:
                cursor.execute(current_rad.insert())
                all_rad.append(current_rad)
            rad_counter += 1
            for i in range(1, len(row.strip()) + 1):
                if row[i - 1] == "x":
                    stol_counter += 1
                    continue
                current_stol = Stol(stol_counter, stol_counter + 1, current_rad)
                exist = False
                for stol in all_stol:
                    if current_stol.stolnr == stol.stolnr and current_stol.rad.radnr == stol.rad.radnr and current_stol.rad.område.navn == stol.rad.område.navn and current_stol.id == stol.id:
                        current_stol = stol
                        exist = True
                        break
                if not exist:
                    print(stol)
                    cursor.execute(current_stol.insert())
                    all_stol.append(current_stol)
                stol_counter += 1


def verifyScenes(conn):
    '''Populate the database with some data'''
    cursor = conn.cursor()
    verifyHovedscene(cursor)
    conn.commit()