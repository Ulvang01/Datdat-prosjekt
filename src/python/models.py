import datetime
import sqlite3
from typing import List, Optional

class Sal:
    def __init__(self, navn: str):
        self.navn = navn

    def __str__(self) -> str:
        return f"Sal(navn={self.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = "INSERT INTO Sal (navn) VALUES (?)"
        cursor.execute(query, (self.navn,))

    def insert_if_not_exists(self, cursor: sqlite3.Cursor) -> bool:
        query = "SELECT * FROM Sal WHERE navn=?"
        cursor.execute(query, (self.navn,))
        if cursor.fetchone() is None:
            self.insert(cursor)
            return True
        return False
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Sal WHERE navn=?"
            cursor.execute(query, (self.navn,))
            return True
        except Exception as e:
            print(f"Error deleting Sal: {e}")
            return False

    
    def get(self, cursor: sqlite3.Cursor) -> Optional['Sal']:
        query = "SELECT * FROM Sal WHERE navn=?"
        cursor.execute(query, (self.navn,))
        row = cursor.fetchone()
        if row:
            return Sal(row[0])
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Sal']:
        cursor.execute("SELECT * FROM Sal")
        return [Sal(row[0]) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, navn: str) -> Optional['Sal']:
        query = "SELECT * FROM Sal WHERE navn=?"
        cursor.execute(query, (navn,))
        row = cursor.fetchone()
        if row:
            return Sal(row[0])
        return None


class Område:
    def __init__(self, id: int, navn: str, sal: Sal):
        self.id = id
        self.navn = navn
        self.sal = sal

    def __str__(self) -> str:
        return f"Område(id={self.id}, navn={self.navn}, sal={self.sal.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = "INSERT INTO Område (navn, sal) VALUES (?, ?)"
        cursor.execute(query, (self.navn, self.sal.navn))

    def insert_if_not_exists(self, cursor: sqlite3.Cursor) -> bool:
        query = "SELECT * FROM Område WHERE navn=? AND sal=?"
        cursor.execute(query, (self.navn, self.sal.navn))
        if cursor.fetchone() is None:
            self.insert(cursor)
            return True
        return False
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Område WHERE navn=? AND sal=?"
            cursor.execute(query, (self.navn, self.sal.navn))
            return True
        except Exception as e:
            print(f"Error deleting Område: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Område SET navn=?, sal=? WHERE id=?"
        cursor.execute(query, (self.navn, self.sal.navn, self.id))

    def get(self, cursor: sqlite3.Cursor) -> Optional['Område']:
        query = "SELECT * FROM Område WHERE navn=? AND sal=?"
        cursor.execute(query, (self.navn, self.sal.navn))
        row = cursor.fetchone()
        if row:
            return Område(row[0], row[1], Sal(row[2]))
        return None
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, områder: List['Område']) -> None:
        query = """
        INSERT INTO Område (navn, sal) VALUES (?, ?)
        ON CONFLICT(navn, sal) DO NOTHING
        """
        values = [(område.navn, område.sal.navn) for område in områder]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Område']:
        query = "SELECT * FROM Område"
        cursor.execute(query)
        return [Område(row[0], row[1], Sal(row[2])) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_sal(cursor: sqlite3.Cursor, sal: Sal) -> List['Område']:
        query = "SELECT * FROM Område WHERE sal=?"
        cursor.execute(query, (sal.navn,))
        return [Område(row[0], row[1], sal) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Område']:
        query = "SELECT * FROM Område WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Område(row[0], row[1], Sal(row[2]))
        return None

class Rad:
    def __init__(self, id: int, radnr: int, område: Område):
        self.id = id
        self.radnr = radnr
        self.område = område

    def __str__(self) -> str:
        return f"Rad(id={self.id}, radnr={self.radnr}, område={self.område.id})"  # Assuming område is an instance of Område
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = "INSERT INTO Rad (id, radnr, område) VALUES (?, ?, ?)"
        cursor.execute(query, (self.id, self.radnr, self.område.id))
    
    def insert_if_not_exists(self, cursor: sqlite3.Cursor) -> bool:
        query = "SELECT * FROM Rad WHERE id = ?"
        cursor.execute(query, (self.id,))
        if cursor.fetchone() is None:
            self.insert(cursor)
            return True
        return False

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Rad WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Rad: {e}")
            return False
    
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Rad SET radnr = ?, område = ? WHERE id = ?"
        cursor.execute(query, (self.radnr, self.område.id, self.id))
    
    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Rad']:
        query = "SELECT * FROM Rad WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            område = Område.get_by_id(cursor, row[2])
            if område:
                return Rad(row[0], row[1], område)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Rad']:
        query = "SELECT * FROM Rad"
        cursor.execute(query)
        rows = cursor.fetchall()
        rader = []
        for row in rows:
            område = Område.get_by_id(cursor, row[2])
            if område:
                rader.append(Rad(row[0], row[1], område))
        return rader
    
    @staticmethod
    def get_by_område(cursor: sqlite3.Cursor, område: Område) -> List['Rad']:
        query = "SELECT * FROM Rad WHERE område = ?"
        cursor.execute(query, (område.id,))
        rows = cursor.fetchall()
        rader = []
        for row in rows:
            rader.append(Rad(row[0], row[1], område))
        return rader
    
    @staticmethod
    def get_by_sal(cursor: sqlite3.Cursor, sal: Sal) -> List['Rad']:
        query = "SELECT * FROM Rad WHERE område IN (SELECT id FROM Område WHERE sal = ?)"
        cursor.execute(query, (sal.navn,))
        rows = cursor.fetchall()
        rader = []
        for row in rows:
            område = Område.get_by_id(cursor, row[2])
            if område:
                rader.append(Rad(row[0], row[1], område))
        return rader

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, rad_list: List['Rad']) -> None:
        query = """
        INSERT INTO Rad (radnr, område) VALUES ( ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(radnr, område) DO NOTHING
        """
        values = [(rad.radnr, rad.område.id) for rad in rad_list]
        cursor.executemany(query, values)

class Stol:
    def __init__(self, id: int, stolnr: int, rad: Rad):
        self.id = id
        self.stolnr = stolnr
        self.rad = rad

    def __str__(self) -> str:
        return f"Stol(id={self.id}, stolnr={self.stolnr}, rad={self.rad.id})"

    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = "INSERT INTO Stol (id, stol_nr, rad) VALUES (?, ?, ?)"
        cursor.execute(query, (self.id, self.stolnr, self.rad.id))

    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Stol SET stol_nr = ?, rad = ? WHERE id = ?"
        cursor.execute(query, (self.stolnr, self.rad.id, self.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Stol WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Stol: {e}")
            return False

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Stol']:
        query = "SELECT * FROM Stol WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            rad = Rad.get_by_id(cursor, row[2]) 
            if rad:
                return Stol(row[0], row[1], rad)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Stol']:
        query = "SELECT * FROM Stol"
        cursor.execute(query)
        rows = cursor.fetchall()
        stoler = []
        for row in rows:
            rad = Rad.get_by_id(cursor, row[2])
            if rad:
                stoler.append(Stol(row[0], row[1], rad))
        return stoler
    
    @staticmethod
    def get_by_sal(cursor: sqlite3.Cursor, sal: Sal) -> List['Stol']:
        query = "SELECT * FROM Stol WHERE rad IN (SELECT id FROM Rad WHERE område IN (SELECT id FROM Område WHERE sal = ?))"
        cursor.execute(query, (sal.navn,))
        rows = cursor.fetchall()
        stoler = []
        for row in rows:
            rad = Rad.get_by_id(cursor, row[2])
            if rad:
                stoler.append(Stol(row[0], row[1], rad))
        return stoler

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, stol_list: List['Stol']) -> None:
        query = """
        INSERT INTO Stol (stol_nr, rad) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(stol_nr, rad) DO NOTHING
        """
        values = [(stol.stolnr, stol.rad.id) for stol in stol_list]
        cursor.executemany(query, values)

class Teaterstykke():
    id: int
    navn: str
    forfatter: str
    tid: datetime.time

    def __init__(self, id: int, navn: str, forfatter: str, tid: datetime.time):
        self.id = id
        self.navn = navn
        self.forfatter = forfatter
        self.tid = tid
    
    def __str__(self):
        return f"Teaterstykke(id={self.id}, navn={self.navn}, forfatter={self.forfatter}, tid={self.tid})"

    def insert(self):
        return f"INSERT INTO Teaterstykke (id, navn, forfatter, tid) VALUES ({self.id}, {self.navn}, {self.forfatter}, {self.tid})"
    
    def update(self):
        return f"UPDATE Teaterstykke SET navn={self.navn}, forfatter={self.forfatter}, tid={self.tid} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Teaterstykke WHERE id={self.id}"

class Visning():
    id: int
    dato: datetime.date
    teaterstykke: Teaterstykke

    def __init__(self, id: int, dato: datetime.date, teaterstykke: Teaterstykke):
        self.id = id
        self.dato = dato
        self.teaterstykke = teaterstykke

    def __str__(self):
        return f"Visning(id={self.id}, dato={self.dato}, teaterstykke={self.teaterstykke})"
    
    def insert(self):
        return f"INSERT INTO Visning (id, dato, teaterstykke) VALUES ({self.id}, {self.dato}, {self.teaterstykke})"
    
    def update(self):
        return f"UPDATE Visning SET dato={self.dato}, teaterstykke={self.teaterstykke} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Visning WHERE id={self.id}"

class BilletPris():
    id: int
    pris: float
    bilettType: str
    teaterstykke: Teaterstykke

    def __init__(self, id: int, pris: float, bilettType: str, teaterstykke: Teaterstykke):
        self.id = id
        self.pris = pris
        self.bilettType = bilettType
        self.teaterstykke = teaterstykke

    def __str__(self):
        return f"BilletPris(id={self.id}, pris={self.pris}, bilettType={self.bilettType}, teaterstykke={self.teaterstykke})"
    
    def insert(self):
        return f"INSERT INTO BilletPris (id, pris, bilettType, teaterstykke) VALUES ({self.id}, {self.pris}, {self.bilettType}, {self.teaterstykke})"
    
    def update(self):
        return f"UPDATE BilletPris SET pris={self.pris}, bilettType={self.bilettType}, teaterstykke={self.teaterstykke} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM BilletPris WHERE id={self.id}"

class KundeProfil():
    id: int
    navn: str
    email: str
    telefon: str

    def __init__(self, id: int, navn: str, email: str, telefon: str):
        self.id = id
        self.navn = navn
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"KundeProfil(id={self.id}, navn={self.navn}, email={self.email}, telefon={self.telefon})"
    
    def insert(self):
        return f"INSERT INTO KundeProfil (id, navn, email, telefon) VALUES ({self.id}, {self.navn}, {self.email}, {self.telefon})"
    
    def update(self):
        return f"UPDATE KundeProfil SET navn={self.navn}, email={self.email}, telefon={self.telefon} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM KundeProfil WHERE id={self.id}"

class BillettKjøp():
    id: int
    time: datetime.time
    dato: datetime.date
    kundeProfile: KundeProfil

    def __init__(self, id: int, time: datetime.time, dato: datetime.date, kundeProfile: KundeProfil):
        self.id = id
        self.time = time
        self.dato = dato
        self.kundeProfile = kundeProfile

    def __str__(self):
        return f"BillettKjøp(id={self.id}, time={self.time}, dato={self.dato}, kundeProfile={self.kundeProfile})"
    
    def insert(self):
        return f"INSERT INTO BillettKjøp (id, time, dato, kundeProfile) VALUES ({self.id}, {self.time}, {self.dato}, {self.kundeProfile})"
    
    def update(self):
        return f"UPDATE BillettKjøp SET time={self.time}, dato={self.dato}, kundeProfile={self.kundeProfile} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM BillettKjøp WHERE id={self.id}"


class Billett():
    id: int
    visning: Visning
    stol: Stol
    billettPris: BilletPris
    billettKjøp: BillettKjøp

    def __init__(self, id: int, visning: Visning, stol: Stol, billettPris: BilletPris, billettKjøp: BillettKjøp):
        self.id = id
        self.visning = visning
        self.stol = stol
        self.billettPris = billettPris
        self.billettKjøp = billettKjøp

    def __str__(self):
        return f"Billett(id={self.id}, visning={self.visning}, stol={self.stol}, billettPris={self.billettPris}, billettKjøp={self.billettKjøp})"
    
    def insert(self):
        return f"INSERT INTO Billett (id, visning, stol, billettPris, billettKjøp) VALUES ({self.id}, {self.visning}, {self.stol}, {self.billettPris}, {self.billettKjøp})"
    
    def update(self):
        return f"UPDATE Billett SET visning={self.visning}, stol={self.stol}, billettPris={self.billettPris}, billettKjøp={self.billettKjøp} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Billett WHERE id={self.id}"


class Akt():
    id: int
    nummer: int
    navn: str

    def __init__(self, id: int, nummer: int, navn: str = None):
        self.id = id
        self.nummer = nummer
        self.navn = navn

    def __str__(self):
        return f"Akt(id={self.id}, nummer={self.nummer}, navn={self.navn})"
    
    def insert(self):
        if self.navn is None or self.navn == "NULL":
            return f"INSERT INTO Akt (id, nummer) VALUES ({self.id}, {self.nummer})"
        else:
            return f"INSERT INTO Akt (id, nummer, navn) VALUES ({self.id}, {self.nummer}, {self.navn})"
    
    def update(self):
        return f"UPDATE Akt SET nummer={self.nummer}, navn={self.navn} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Akt WHERE id={self.id}"
    

class Skuespiller():
    id: int
    navn: str

    def __init__(self, id: int, navn: str):
        self.id = id
        self.navn = navn
    
    def __str__(self):
        return f"Skuespiller(id={self.id}, navn={self.navn})"
    
    def insert(self):
        return f"INSERT INTO Skuespiller (id, navn) VALUES ({self.id}, {self.navn})"
    
    def update(self):
        return f"UPDATE Skuespiller SET navn={self.navn} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Skuespiller WHERE id={self.id}; DELETE FROM SkuespillerRolleJunction WHERE skuespiller={self.id}"

class Roller():
    id: int
    navn: str

    def __init__(self, id: int, navn: str):
        self.id = id
        self.navn = navn

    def __str__(self):
        return f"Roller(id={self.id}, navn={self.navn})"
    
    def insert(self):
        return f"INSERT INTO Roller (id, navn) VALUES ({self.id}, {self.navn})"
    
    def update(self):
        return f"UPDATE Roller SET navn={self.navn} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Roller WHERE id={self.id}; DELETE FROM AktRolleJunction WHERE rolle={self.id}; DELETE FROM SkuespillerRolleJunction WHERE rolle={self.id}"
    

class AktRolleJunction():
    akt: Akt
    rolle: Roller

    def __init__(self, akt: Akt, rolle: Roller):
        self.akt = akt
        self.rolle = rolle

    def __str__(self):
        return f"AktRolleJunction(akt={self.akt}, rolle={self.rolle})"
    
    def insert(self):
        return f"INSERT INTO AktRolleJunction (akt, rolle) VALUES ({self.akt}, {self.rolle})"
    
    def delete(self):
        return f"DELETE FROM AktRolleJunction WHERE akt={self.akt} AND rolle={self.rolle}"
    

class SkuespillerRolleJunction():
    skuespiller: Skuespiller
    rolle: Roller

    def __init__(self, skuespiller: Skuespiller, rolle: Roller):
        self.skuespiller = skuespiller
        self.rolle = rolle

    def __str__(self):
        return f"SkuespillerRolleJunction(skuespiller={self.skuespiller}, rolle={self.rolle})"
    
    def insert(self):
        return f"INSERT INTO SkuespillerRolleJunction (skuespiller, rolle) VALUES ({self.skuespiller}, {self.rolle})"
    
    def delete(self):
        return f"DELETE FROM SkuespillerRolleJunction WHERE skuespiller={self.skuespiller} AND rolle={self.rolle}"

class Oppgave():
    id: int
    navn: str
    beskrivelse: str
    teaterstykke: Teaterstykke

    def __init__(self, id: int, navn: str, beskrivelse: str, teaterstykke: Teaterstykke):
        self.id = id
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.teaterstykke = teaterstykke

    def __str__(self):
        return f"Oppgave(id={self.id}, navn={self.navn}, beskrivelse={self.beskrivelse}, teaterstykke={self.teaterstykke})"
    
    def insert(self):
        return f"INSERT INTO Oppgave (id, navn, beskrivelse, teaterstykke) VALUES ({self.id}, {self.navn}, {self.beskrivelse}, {self.teaterstykke})"
    
    def update(self):
        return f"UPDATE Oppgave SET navn={self.navn}, beskrivelse={self.beskrivelse}, teaterstykke={self.teaterstykke} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Oppgave WHERE id={self.id}"

class AnsattStatus():
    status: str

    def __init__(self, status: str):
        self.status = status

    def __str__(self):
        return f"AnsattStatus(status={self.status})"
    
    def insert(self):
        return f"INSERT INTO AnsattStatus (status) VALUES ({self.status})"
    
    def delete(self):
        return f"DELETE FROM AnsattStatus WHERE status={self.status}"

class StillingsTittel():
    tittel: str

    def __init__(self, tittel: str):
        self.tittel = tittel

    def __str__(self):
        return f"StillingsTittel(tittel={self.tittel})"
    
    def insert(self):
        return f"INSERT INTO StillingsTittel (tittel) VALUES ({self.tittel})"
    
    def delete(self):
        return f"DELETE FROM StillingsTittel WHERE tittel={self.tittel}"

class Medvirkende():
    id: int
    navn: str
    email: str
    status: AnsattStatus
    stilling: StillingsTittel

    def __init__(self, id: int, navn: str, email: str, status: AnsattStatus, stilling: StillingsTittel=None):
        self.id = id
        self.navn = navn
        self.email = email
        self.status = status
        self.stilling = stilling

    def __str__(self):
        return f"Medvirkende(id={self.id}, navn={self.navn}, email={self.email}, status={self.status}, stilling={self.stilling})"
    
    def insert(self):
        if self.stilling is None:
            return f"INSERT INTO Medvirkende (id, navn, email, status) VALUES ({self.id}, {self.navn}, {self.email}, {self.status})"
        else:
            return f"INSERT INTO Medvirkende (id, navn, email, status, stilling) VALUES ({self.id}, {self.navn}, {self.email}, {self.status}, {self.stilling})"
    
    def update(self):
        if self.stilling is None:
            return f"UPDATE Medvirkende SET navn={self.navn}, email={self.email}, status={self.status} WHERE id={self.id}"
        else:
            return f"UPDATE Medvirkende SET navn={self.navn}, email={self.email}, status={self.status}, stilling={self.stilling} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Medvirkende WHERE id={self.id}"

class SkuespillerOppgaveJunction():
    skuespiller: Skuespiller
    oppgave: Oppgave

    def __init__(self, skuespiller: Skuespiller, oppgave: Oppgave):
        self.skuespiller = skuespiller
        self.oppgave = oppgave

    def __str__(self):
        return f"SkuespillerOppgaveJunction(skuespiller={self.skuespiller}, oppgave={self.oppgave})"
    
    def insert(self):
        return f"INSERT INTO SkuespillerOppgaveJunction (skuespiller, oppgave) VALUES ({self.skuespiller}, {self.oppgave})"
    
    def delete(self):
        return f"DELETE FROM SkuespillerOppgaveJunction WHERE skuespiller={self.skuespiller} AND oppgave={self.oppgave}"
    
