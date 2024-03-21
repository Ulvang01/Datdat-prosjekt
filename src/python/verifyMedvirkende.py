import os

from src.python.models import AnsattStatus, Medvirkende, Oppgave, OppgaveMedvirkendeJunctoin, Teaterstykket

ansattStatusPath = os.path.join("src", "res", "ansattstatus.txt")
stillingsTittelPath = os.path.join("src", "res", "medvirkende.txt")

def verifyStatus(cursor):
    """ Verify AnsattStatus in database"""
    try:
        cursor.execute("BEGIN;")
        with open(ansattStatusPath, 'r') as file:
            print("Reading ansattstatus...")
            content = file.readlines()
        
        ansattStatus_list = []
        for i in range(len(content)):
            ansattStatus_list.append(AnsattStatus(content[i].strip()))
        
        AnsattStatus.upsert_batch(cursor, ansattStatus_list)
        cursor.execute("COMMIT;")
        print("Done verifying ansattstatus...")

    except Exception as e:
        print("Error verifying ansattstatus...")
        print(e)
        cursor.execute("ROLLBACK;")
        return
    
def verifyMedvirkende(cursor):
    """ Verify StillingsTittel in database"""
    try:
        cursor.execute("BEGIN;")
        with open(stillingsTittelPath, 'r') as file:
            print("Reading medvirkende...")
            content = file.readlines()
        
        content = [x.split(":") for x in content]
        
        for i in range(len(content)):
            print("Verifying medvirkende...")
            medvirkende = Medvirkende(None, content[i][0].strip(), "null", AnsattStatus.get_by_status(cursor, "ansatt"))
            medvirkende.insert(cursor)
            medvirkende = Medvirkende.get_by_name(cursor, medvirkende.navn)
            oppgaver = content[i][1].split("/")
            for o in oppgaver:
                oppgave = Oppgave.get_by_name_and_teaterstykket(cursor, o.strip(), Teaterstykket.get_by_name(cursor, content[i][2].strip()))
                if oppgave is None or oppgave.id is None:
                    oppgave = Oppgave(None, o.strip(), Teaterstykket.get_by_name(cursor, content[i][2].strip()))
                    oppgave.insert(cursor)
                    oppgave = Oppgave.get_by_name_and_teaterstykket(cursor, oppgave.navn, oppgave.teaterstykket)
                junction = OppgaveMedvirkendeJunctoin(medvirkende, oppgave)
                junction.insert(cursor)

        cursor.execute("COMMIT;")
        print("Done verifying medvirkende...")
    except Exception as e:
        print("Error verifying medvirkende...")
        print(e.with_traceback(e.__traceback__))
        cursor.execute("ROLLBACK;")
        return

def verifyMedvirkendeAndStatus(conn):
    cursor = conn.cursor()
    verifyStatus(cursor)
    verifyMedvirkende(cursor)
    conn.commit()