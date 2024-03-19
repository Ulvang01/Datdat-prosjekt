import re
import os

from src.python.models import Sal, Teaterstykket, Visning, BillettPris, Akt, Skuespiller, Roller, SkuespillerRolleJunction, RolleAkterJunction
from datetime import datetime

avspillingPath = os.path.join("src", "res", "avspillingsdager.txt")
kongsemnenePirsPath = os.path.join("src", "res", "priser-Kongsemnene.txt")

kongsemneneMedvirkendePath = os.path.join("src", "res", "skuespillere-Kongsemnene.txt")
størstAvAltErKjærlighetenPirsPath = os.path.join('src', 'res', 'priser-Størst_av_alt_er_kjærligheten.txt')
størstAvAltErKjærlighetenMedvirkendePath = os.path.join('src', 'res', 'skuespillere-Størst_av_alt_er_kjærligheten.txt')
rollerKongsemnene = os.path.join("src", "res", "roller-Kongsemnene.txt")
rollerStørstAvAltErKjærlighten = os.path.join('src', 'res', 'roller-Størst_av_alt_er_kjærligheten.txt')

def verifyKongsemnene(cursor):
    """Verify the database with teaterstykke Kongsemnene"""
    print("Verifying Kongsemnene...")

    try:
        cursor.execute("BEGIN;")
        with open(avspillingPath, 'r') as file:
            print("Reading Kongsemnene...")
            content = file.readlines()[0].split(" ")

        sal = Sal.get_by_name(cursor, "Hovedscene")
        teaterstykke = Teaterstykket(1, "Kongsemnene", "Henrik Ibsen", content[1], sal)
        teaterstykke.insert(cursor)

        print("Verifying visninger...")
        vising_list = []
        for i in range(2, len(content)):
            full_date = content[i] + " 2024"
            dateobj = datetime.strptime(full_date, "%d.%b %Y")
            sql_date = dateobj.strftime("%Y-%m-%d")
            vising_list.append(Visning(None, sql_date, teaterstykke))

        Visning.upsert_batch(cursor, vising_list)

        print("Verifying billettpriser...")
        with open(kongsemnenePirsPath, 'r') as file:
            print("Reading Kongsemnene priser...")
            content = file.readlines()

        billettpris_list = []
        for i in range(len(content)):
            billettpris_list.append(BillettPris(None, content[i].split(": ")[1], content[i].split(": ")[0], teaterstykke))

        BillettPris.upsert_batch(cursor, billettpris_list)


        print("Verifying skuespillere...")
        with open(kongsemneneMedvirkendePath, 'r') as file:
            print("Reading Kongsemnene skuespillere...")
            content = file.readlines()
        
            
        for i in range(len(content)):
            navn = content[i].split(" : ")[0]
            rolle = content[i].split(" : ")[1].strip().split(" / ")
            for r in rolle:
                if not Roller.get_by_name(cursor, r):
                    roller = Roller(None, r)
                    roller.insert(cursor)
                skuespiller = Skuespiller.get_by_name(cursor, navn)
                if not skuespiller:
                    skuespiller = Skuespiller(None, navn)
                    skuespiller.insert(cursor)
                skuespillerRolleJunction = SkuespillerRolleJunction(Skuespiller.get_by_name(cursor, navn), Roller.get_by_name(cursor, r))
                skuespillerRolleJunction.insert(cursor)

        print("Verifying akter...")
        with open(rollerKongsemnene, 'r') as file:
            print("Reading roller i Kongsemnene...")
            content = file.readlines()[1:]

        akt_list = []
        for i in range(5):
            akt_list.append(Akt(None, i + 1, teaterstykke))
        
        Akt.upsert_batch(cursor, akt_list)
        
        for line in content:
            rollenavn = line.split(" : ")[0]
            akter = line.split(" : ")[1].strip().split(", ")
            for a in akter:
                akt = Akt.get_by_nummer_and_teaterstykket(cursor, int(a), teaterstykke)
                if not akt:
                    akt = Akt(None, int(a), teaterstykke)
                    akt.insert(cursor)
                rolle = Roller.get_by_name(cursor, rollenavn)
                if not rolle:
                    rolle = Roller(None, rollenavn)
                    rolle.insert(cursor)
                aktRolleJunction = RolleAkterJunction(akt, Roller.get_by_name(cursor, rollenavn))
                aktRolleJunction.insert(cursor)

        cursor.execute("COMMIT;")
    except Exception as e:
        print("Error verifying Kongsemnene...")
        print(e)
        cursor.execute("ROLLBACK;")
        return

def verifyStørstAvAltErKjærligheten(cursor):
    """Verify the database with teaterstykke Kongsemnene"""
    print("Verifying Størst av alt er kjærligheten...")

    try:
        cursor.execute("BEGIN;")
        with open(avspillingPath, 'r') as file:
            print("Reading Størst av alt er kjærligheten...")
            content = file.readlines()[1].split(" ")

        sal = Sal.get_by_name(cursor, "Gamle-scene")
        teaterstykke = Teaterstykket(2, "Størst av alt er kjærligheten", "Jonas Corell Petersen", content[1], sal)
        teaterstykke.insert(cursor)

        print("Verifying visninger...")
        vising_list = []
        for i in range(2, len(content)):
            full_date = content[i] + " 2024"
            dateobj = datetime.strptime(full_date, "%d.%b %Y")
            sql_date = dateobj.strftime("%Y-%m-%d")
            vising_list.append(Visning(None, sql_date, teaterstykke))

        Visning.upsert_batch(cursor, vising_list)

        print("Verifying billettpriser...")
        with open(størstAvAltErKjærlighetenPirsPath, 'r') as file:
            print("Reading Størst_av_alt_er_kjærligheten priser...")
            content = file.readlines()

        billettpris_list = []
        for i in range(len(content)):
            billettpris_list.append(BillettPris(None, content[i].split(": ")[1], content[i].split(": ")[0], teaterstykke))

        BillettPris.upsert_batch(cursor, billettpris_list)


        print("Verifying skuespillere...")
        with open(kongsemneneMedvirkendePath, 'r') as file:
            print("Reading Størst_av_alt_er_kjærligheten skuespillere...")
            content = file.readlines()

        for i in range(len(content)):
            navn = content[i].split(" : ")[0]
            rolle = content[i].split(" : ")[1].strip().split(" / ")
            for r in rolle:
                if not Roller.get_by_name(cursor, r):
                    roller = Roller(None, r)
                    roller.insert(cursor)
                skuespiller = Skuespiller.get_by_name(cursor, navn)
                if not skuespiller:
                    skuespiller = Skuespiller(None, navn)
                    skuespiller.insert(cursor)
                skuespillerRolleJunction = SkuespillerRolleJunction(Skuespiller.get_by_name(cursor, navn), Roller.get_by_name(cursor, r))
                skuespillerRolleJunction.insert(cursor)

        print("Verifying akter...")
        with open(rollerStørstAvAltErKjærlighten, 'r') as file:
            print("Reading roller i Størst_av_alt_er_kjærligheten...")
            content = file.readlines()[1:]

        akt_list = []
        for i in range(1):
            akt_list.append(Akt(None, i + 1, teaterstykke))
        
        Akt.upsert_batch(cursor, akt_list)
        
        for line in content:
            rollenavn = line.split(" : ")[0]
            akter = line.split(" : ")[1].strip().split(", ")
            for a in akter:
                akt = Akt.get_by_nummer_and_teaterstykket(cursor, int(a), teaterstykke)
                if not akt:
                    akt = Akt(None, int(a), teaterstykke)
                    akt.insert(cursor)
                rolle = Roller.get_by_name(cursor, rollenavn)
                if not rolle:
                    rolle = Roller(None, rollenavn)
                    rolle.insert(cursor)
                aktRolleJunction = RolleAkterJunction(akt, Roller.get_by_name(cursor, rollenavn))
                aktRolleJunction.insert(cursor)

        cursor.execute("COMMIT;")
    except Exception as e:
        print("Error verifying Størst_av_alt_er_kjærligheten...")
        print(e)
        cursor.execute("ROLLBACK;")
        return
    
def verifyTeaterstykkene(conn):
    '''Verify the database with the teaterstykker'''
    cursor = conn.cursor()
    verifyKongsemnene(cursor)
    verifyStørstAvAltErKjærligheten(cursor)
    conn.commit()
    print('Teaterstykker verified')
    return
