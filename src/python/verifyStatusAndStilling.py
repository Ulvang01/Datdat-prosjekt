import os

from src.python.models import AnsattStatus, StillingsTittel

ansattStatusPath = os.path.join("src", "res", "ansattstatus.txt")
stillingsTittelPath = os.path.join("src", "res", "stillinger.txt")

def verifyStilling(cursor):
    """ Verify AnsattStatus in database"""
    cursor.execute("BEGIN;")
    with open(ansattStatusPath, 'r') as file:
        print("Reading ansattstatus...")
        content = file.readlines()
    
    ansattStatus_list = []
    for i in range(len(content)):
        ansattStatus_list.append(AnsattStatus(content[i].strip()))
    
    AnsattStatus.upsert_batch(cursor, ansattStatus_list)

def verifyStillinger(cursor):
    """ Verify StillingsTittel in database"""
    cursor.execute("BEGIN;")
    with open(stillingsTittelPath, 'r') as file:
        print("Reading stillinger...")
        content = file.readlines()
    
    stillingsTittel_list = []
    for i in range(len(content)):
        stillingsTittel_list.append(StillingsTittel(content[i].strip()))
    
    StillingsTittel.upsert_batch(cursor, stillingsTittel_list)


def verifyStillingAndStatus(conn):
    cursor = conn.cursor()
    verifyStilling(cursor)
    verifyStillinger(cursor)
    conn.commit()