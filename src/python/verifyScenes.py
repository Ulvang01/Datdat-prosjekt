import sqlite3
from src.python.models import Scene, Area, Row, Chair
import re
import os

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")

def processArea(content, scene, cursor):
    area_list = []

    for row in content:
        if not bool(re.search(r'\d', row)) and row.strip() != "":
            area_list.append(Area(None, row.strip(), scene))

    Area.upsert_batch(cursor, area_list)
    return Area.get_by_scene(cursor, scene)

def getRows(cursor, content, area_list):
    rows = []
    area_count = 0
    row_count = 1
    for i in range(len(content)):
        if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
            area_count += 1
            row_count = 1
        else:
            rows.append(Row(None, row_count, area_list[area_count]))
            row_count += 1
    Row.upsert_batch(cursor, rows)
    return rows

def getChairList(cursor, content, rows, chairPerRow: bool):
    charis = []
    chair_count = 1
    row_count = 0
    area_count = 0
    for i in range(len(content)):
            if bool(re.fullmatch(r'[A-Za-z]+', content[i].strip())):
                area_count += 1
            else:
                for j in range(len(content[i].strip())):
                    if content[i][j] != 'x':
                        charis.append(Chair(None, chair_count, Row.get_by_area_and_row_num(cursor, rows[row_count].area, rows[row_count].row_num)))
                    chair_count += 1
                row_count += 1
                if chairPerRow:
                    chair_count = 1
    Chair.upsert_batch(cursor, charis)
    return charis

def deleteUnverifiedArea(cursor, area_list, scene):
    for db_area in Area.get_by_scene(cursor, scene):
        should_delete = True
        for txt_area in area_list:
            if db_area.name == txt_area.name and db_area.scene == txt_area.scene:
                should_delete = False
        if should_delete:
            db_area.delete(cursor)

def deleteUnverifiedRow(cursor, rows, scene):
    for db_row in Row.get_by_scene(cursor, scene):
        should_delete = True
        for txt_row in rows:
            if db_row.row_num == txt_row.row_num and db_row.area.id == txt_row.area.id:
                should_delete = False
        if should_delete:
            db_row.delete(cursor)

def deleteUnverifiedChair(cursor, chair_list, scene):
    for db_chair in Chair.get_by_scene(cursor, scene):
        should_delete = True
        for txt_chair in chair_list:
            if db_chair.chair_num == txt_chair.chair_num and db_chair.row.id == txt_chair.row.id:
                should_delete = False
        if should_delete:
            db_chair.delete(cursor)

def veifyScene(cursor, path, scene):
    '''Verify a scene'''
    try:
        cursor.execute("BEGIN;")
        
        scene = Scene(scene)
        scene.insert(cursor)
        
        with open(path, 'r') as file:
            print(f"Reading {scene}...")
            content = file.readlines()[1:]

        content = content[::-1]
        area_list = processArea(content, scene, cursor)
        rows = getRows(cursor, content, area_list)
        
        if scene.name == "Hovedscene":
            chair_list = getChairList(cursor, content, rows, False)
        else:
            chair_list = getChairList(cursor, content, rows, True)

        deleteUnverifiedArea(cursor, area_list, scene)
        deleteUnverifiedRow(cursor, rows, scene)
        deleteUnverifiedChair(cursor, chair_list, scene)

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