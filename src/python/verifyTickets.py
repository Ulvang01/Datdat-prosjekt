import re
import os

from src.python.models import * # TODO: only the models I need

avspillingPath = os.path.join("src", "res", "avspillingsdager.txt")
kongsemnenePirsPath = os.path.join("src", "res", "priser-Kongsemnene.txt")

hovedScenePath = os.path.join("src", "res", "hovedscenen.txt")
gamleScenePath = os.path.join("src", "res", "gamle-scene.txt")

def verifyUser(cursor):
    pass

def verifyHovedscenePurchase(cursor):
    pass

def verifyGamlescenePurchase(cursor):
    pass

def verifyTickets(conn):
    cursor = conn.cursor()
    verifyUser(cursor)
    verifyHovedscenePurchase(cursor)
    verifyGamlescenePurchase(cursor)
    conn.commit()