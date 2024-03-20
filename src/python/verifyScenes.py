import sqlite3
from src.python.models import Sal, Område, Rad, Stol
import re
import os

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")

def processOmråde(content, scene, cursor):
    område_list = []

    for row in content:
        if not bool(re.search(r'\d', row)) and row.strip() != "":
            område_list.append(Område(None, row.strip(), scene))

    Område.upsert_batch(cursor, område_list)
    return Område.get_by_sal(cursor, scene)

def getRows(cursor, content, område_list):
    rows = []
    område_count = 0
    rad_count = 1
    for i in range(len(content)):
        if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
            område_count += 1
            rad_count = 1
        else:
            rows.append(Rad(None, rad_count, område_list[område_count]))
            rad_count += 1
    Rad.upsert_batch(cursor, rows)
    return rows

def getChairList(cursor, content, rows, chairPerRow: bool):
    charis = []
    stol_count = 1
    rad_count = 0
    område_count = 0
    for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                område_count += 1
            else:
                for j in range(len(content[i].strip())):
                    if content[i][j] != 'x':
                        charis.append(Stol(None, stol_count, Rad.get_by_område_and_radnr(cursor, rows[rad_count].område, rows[rad_count].radnr)))
                    stol_count += 1
                rad_count += 1
                if not chairPerRow:
                    stol_count = 1
    Stol.upsert_batch(cursor, charis)
    return charis

def deleteUnverifiedOmråde(cursor, område_list, scene):
    for db_område in Område.get_by_sal(cursor, scene):
        should_delete = True
        for txt_område in område_list:
            if db_område.navn == txt_område.navn and db_område.sal == txt_område.sal:
                should_delete = False
        if should_delete:
            db_område.delete(cursor)

def deleteUnverifiedRad(cursor, rows, scene):
    for db_rad in Rad.get_by_sal(cursor, scene):
        should_delete = True
        for txt_rad in rows:
            if db_rad.radnr == txt_rad.radnr and db_rad.område.id == txt_rad.område.id:
                should_delete = False
        if should_delete:
            db_rad.delete(cursor)

def deleteUnverifiedStol(cursor, stol_list, scene):
    for db_stol in Stol.get_by_sal(cursor, scene):
        should_delete = True
        for txt_stol in stol_list:
            if db_stol.stolnr == txt_stol.stolnr and db_stol.rad.id == txt_stol.rad.id:
                should_delete = False
        if should_delete:
            db_stol.delete(cursor)

def veifyScene(cursor, path, scene):
    '''Verify a scene'''
    try:
        cursor.execute("BEGIN;")
        
        scene = Sal(scene)
        scene.insert(cursor)
        
        with open(path, 'r') as file:
            print(f"Reading {scene}...")
            content = file.readlines()[1:]

        content = content[::-1]
        område_list = processOmråde(content, scene, cursor)
        rows = getRows(cursor, content, område_list)

        if scene == "Hovedscene":
            stol_list = getChairList(cursor, content, rows, False)
        else:
            stol_list = getChairList(cursor, content, rows, True)

        deleteUnverifiedOmråde(cursor, område_list, scene)
        deleteUnverifiedRad(cursor, rows, scene)
        deleteUnverifiedStol(cursor, stol_list, scene)

        cursor.execute("COMMIT;")
        print(f"{scene} verified.")
        return
    except Exception as e:
        print(f"Failed to verify {scene}.")
        print(e.with_traceback())
        cursor.execute("ROLLBACK;")
        return


def verifyScenes(conn):
    '''Populate databasen with some data'''
    cursor = conn.cursor()
    veifyScene(cursor, hovedScenePath, "Hovedscene")
    conn.commit()
    veifyScene(cursor, gamleScenePath, "Gamle-scene")
    conn.commit()