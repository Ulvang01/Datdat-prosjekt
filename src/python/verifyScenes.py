from models import Sal, Område, Rad, Stol
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

def verifyHovedscene(cursor):
    '''Verify the database with the hovedsal'''
    print("Verifying hovedscene...")

    try:
        cursor.execute("BEGIN;")
        
        hovedScene = Sal("Hovedscene")
        hovedScene.insert_if_not_exists(cursor)
        
        with open(hovedScenePath, 'r') as file:
            print("Reading hovedscene...")
            content = file.readlines()[1:]

        område_list = processOmråde(content, hovedScene, cursor)
        content = content[::-1]

        område_count = 0
        rad_list = []
        rad_count = 1
        for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                område_count += 1
                rad_count = 1
            else:
                rad_list.append(Rad(None, rad_count, område_list[område_count]))
                rad_count += 1

        Rad.upsert_batch(cursor, rad_list)
        all_rads = Rad.get_by_sal(cursor, hovedScene)


        stol_list = []
        stol_count = 1
        rad_count = 0
        område_count = 0
        for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                område_count += 1
            else:
                for j in range(len(content[i].strip())):
                    if content[i][j] != 'x':
                        stol_list.append(Stol(None, stol_count, all_rads[rad_count]))
                    stol_count += 1
                rad_count += 1
        Stol.upsert_batch(cursor, stol_list)

        if len(område_list) != len(Område.get_by_sal(cursor, hovedScene)):
            for db_område in Område.get_by_sal(cursor, hovedScene):
                should_delete = True
                for txt_område in område_list:
                    if db_område.navn == txt_område.navn and db_område.sal == txt_område.sal:
                        should_delete = False
                if should_delete:
                    db_område.delete(cursor)
        
        if len(rad_list) != len(Rad.get_by_sal(cursor, hovedScene)):
            for db_rad in Rad.get_by_sal(cursor, hovedScene):
                should_delete = True
                for txt_rad in rad_list:
                    if db_rad.radnr == txt_rad.radnr and db_rad.område == txt_rad.område:
                        should_delete = False
        
        if len(stol_list) != len(Stol.get_by_sal(cursor, hovedScene)):
            for db_stol in Stol.get_by_sal(cursor, hovedScene):
                should_delete = True
                for txt_stol in stol_list:
                    if db_stol.stolnr == txt_stol.stolnr and db_stol.rad.id == txt_stol.rad.id:
                        should_delete = False
                if should_delete:
                    db_stol.delete(cursor)

        cursor.execute("COMMIT;")
        print("Hovedscene verified.")
    except Exception as e:
        print("Failed to verify hovedscene.")
        print(e)
        cursor.execute("ROLLBACK;")
        return

def verifyGameleScene(cursor):
    """Verify the database with the gamle scene"""
    print("Verifying gamle scene...")

    try:
        cursor.execute("BEGIN;")
        
        gamleScene = Sal("Gamle-scene")
        gamleScene.insert_if_not_exists(cursor)
        
        with open(gamleScenePath, 'r') as file:
            print("Reading gamle scene...")
            content = file.readlines()[1:]
        
        område_list = processOmråde(content, gamleScene, cursor)
        content = content[::-1]

        område_count = 0
        rad_list = []
        rad_count = 1
        for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                område_count += 1
                rad_count = 1
            else:
                rad_list.append(Rad(None, rad_count, område_list[område_count]))
                rad_count += 1
        
        Rad.upsert_batch(cursor, rad_list)
        all_rads = Rad.get_by_sal(cursor, gamleScene)

        stol_list = []
        rad_count = 0
        område_count = 0
        for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                område_count += 1
            else:
                for j in range(len(content[i].strip())):
                    if content[i][j] != 'x':
                        stol_list.append(Stol(None, j+1, all_rads[rad_count]))
                rad_count += 1
        
        Stol.upsert_batch(cursor, stol_list)

        if len(område_list) != len(Område.get_by_sal(cursor, gamleScene)):
            for db_område in Område.get_by_sal(cursor, gamleScene):
                should_delete = True
                for txt_område in område_list:
                    if db_område.navn == txt_område.navn and db_område.sal == txt_område.sal:
                        should_delete = False
                if should_delete:
                    db_område.delete(cursor)

        if len(rad_list) != len(Rad.get_by_sal(cursor, gamleScene)):
            for db_rad in Rad.get_by_sal(cursor, gamleScene):
                should_delete = True
                for txt_rad in rad_list:
                    if db_rad.radnr == txt_rad.radnr and db_rad.område == txt_rad.område:
                        should_delete = False

        if len(stol_list) != len(Stol.get_by_sal(cursor, gamleScene)):
            for db_stol in Stol.get_by_sal(cursor, gamleScene):
                should_delete = True
                for txt_stol in stol_list:
                    if db_stol.stolnr == txt_stol.stolnr and db_stol.rad.id == txt_stol.rad.id:
                        should_delete = False
                if should_delete:
                    db_stol.delete(cursor)

        cursor.execute("COMMIT;")
        print("Gamle scene verified.")
    except Exception as e:
        print("Failed to verify gamle scene.")
        print(e)
        cursor.execute("ROLLBACK;")
        return

def verifyScenes(conn):
    '''Populate the database with some data'''
    cursor = conn.cursor()
    verifyHovedscene(cursor)
    verifyGameleScene(cursor)
    conn.commit()