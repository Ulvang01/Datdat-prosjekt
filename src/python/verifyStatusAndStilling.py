import os
from models import AnsattStatus, StillingsTittel

ansattStatusPath = os.path.join("src", "res", "ansattstatus.txt")

def verifyStilling(cursor):
    """ Verify AnsattStatus in database"""


def verifyStillingAndStatus(conn):
    cursor = conn.cursor()
