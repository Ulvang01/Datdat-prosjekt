import datetime
import sqlite3
from typing import List, Optional

class Sal:
    def __init__(self, navn: str):
        self.navn = navn

    def __str__(self) -> str:
        return f"Sal(navn={self.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Sal (navn) VALUES (?)
        ON CONFLICT(navn) DO NOTHING
        """
        cursor.execute(query, (self.navn,))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Sal WHERE navn=?"
            cursor.execute(query, (self.navn,))
            return True
        except Exception as e:
            print(f"Error deleting Sal: {e}")
            return False

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

    def __repr__(self) -> str:
        return f"Område(id={self.id}, navn={self.navn}, sal={self.sal.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Område (navn, sal) VALUES (?, ?)
        ON CONFLICT(navn, sal) DO NOTHING
        """
        cursor.execute(query, (self.navn, self.sal.navn))
    
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
        return [Område(row[0], row[1], Sal.get_by_name(row[2])) for row in cursor.fetchall()]
    
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
            sal = Sal.get_by_name(cursor, row[2])
            if sal:
                return Område(row[0], row[1], sal)
        return None

class Rad:
    def __init__(self, id: int, radnr: int, område: Område):
        self.id = id
        self.radnr = radnr
        self.område = område

    def __str__(self) -> str:
        return f"Rad(id={self.id}, radnr={self.radnr}, område={self.område.id})"  # Assuming område is an instance of Område
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Rad (id, radnr, område) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.radnr, self.område.id))

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

class Teaterstykket():
    def __init__(self, id: int, navn: str, forfatter: str, tid: str, sal: Sal):
        self.id = id
        self.navn = navn
        self.forfatter = forfatter
        self.tid = tid
        self.sal = sal
    
    def __str__(self):
        return f"teaterstykket(id={self.id}, navn={self.navn}, forfatter={self.forfatter}, tid={self.tid})"

    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Teaterstykket (id, navn, forfatter, tid, sal) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.navn, self.forfatter, self.tid, self.sal.navn))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Teaterstykket WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Teaterstykket: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Teaterstykket SET navn = ?, forfatter = ?, tid = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.forfatter, self.tid, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Teaterstykket']:
        query = "SELECT * FROM Teaterstykket WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Teaterstykket(row[0], row[1], row[2], row[3], row[4])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Teaterstykket']:
        query = "SELECT * FROM Teaterstykket"
        cursor.execute(query)
        rows = cursor.fetchall()
        teaterstykker = []
        for row in rows:
            teaterstykker.append(Teaterstykket(row[0], row[1], row[2], row[3]))
        return teaterstykker
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, teaterstykke_list: List['Teaterstykket']) -> None:
        query = """
        INSERT INTO Teaterstykket (navn, forfatter, tid) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(navn, forfatter) DO NOTHING
        """
        values = [(teaterstykket.navn, teaterstykket.forfatter, teaterstykket.tid) for teaterstykket in teaterstykke_list]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str):
        query = """
        SELECT * FROM Teaterstykket WHERE navn = ?
        """
        cursor.execute(query, (name,))
        teaterstykket = cursor.fetchone()
        if teaterstykket:
            return Teaterstykket(teaterstykket[0], teaterstykket[1], teaterstykket[2], teaterstykket[3], teaterstykket[4])
        return None


class Visning():
    id: int
    dato: datetime.date
    teaterstykket: Teaterstykket

    def __init__(self, id: int, dato: datetime.date, teaterstykket: Teaterstykket):
        self.id = id
        self.dato = dato
        self.teaterstykket = teaterstykket

    def __str__(self):
        return f"Visning(id={self.id}, dato={self.dato}, teaterstykket={self.teaterstykket})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Visning (id, dato, teaterstykket) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.dato, self.teaterstykket.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Visning WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Visning: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Visning SET dato = ?, teaterstykket = ? WHERE id = ?"
        cursor.execute(query, (self.dato, self.teaterstykket.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Visning']:
        query = "SELECT * FROM Visning WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Visning(row[0], row[1], Teaterstykket.get_by_id(cursor, row[2]))
        return None
    
    @staticmethod
    def get_by_dato_and_teaterstykke(cursor: sqlite3.Cursor, dato: datetime.date, teaterstykket: Teaterstykket) -> Optional['Visning']:
        query = "SELECT * FROM Visning WHERE dato = ? AND teaterstykket = ?"
        cursor.execute(query, (dato, teaterstykket.id))
        row = cursor.fetchone()
        if row:
            return Visning(row[0], row[1], teaterstykket)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Visning']:
        query = "SELECT * FROM Visning"
        cursor.execute(query)
        rows = cursor.fetchall()
        visninger = []
        for row in rows:
            visninger.append(Visning(row[0], row[1], Teaterstykket.get_by_id(cursor, row[2])))
        return visninger
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, visning_list: List['Visning']) -> None:
        query = """
        INSERT INTO Visning (dato, teaterstykket) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(dato, teaterstykket) DO NOTHING
        """
        values = [(visning.dato, visning.teaterstykket.id) for visning in visning_list]
        cursor.executemany(query, values)

class BillettPris():
    def __init__(self, id: int, pris: float, bilettType: str, teaterstykket: Teaterstykket):
        self.id = id
        self.pris = pris
        self.bilettType = bilettType
        self.teaterstykket = teaterstykket

    def __str__(self):
        return f"BillettPris(id={self.id}, pris={self.pris}, billett_type={self.bilettType}, teaterstykket={self.teaterstykket})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO BillettPris (id, pris, billett_type, teaterstykket) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.pris, self.bilettType, self.teaterstykket.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM BillettPris WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting BillettPris: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE BillettPris SET pris = ?, billett_type = ?, teaterstykket = ? WHERE id = ?"
        cursor.execute(query, (self.pris, self.bilettType, self.teaterstykket.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['BillettPris']:
        query = "SELECT * FROM BillettPris WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return BillettPris(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['BillettPris']:
        query = "SELECT * FROM BillettPris"
        cursor.execute(query)
        rows = cursor.fetchall()
        billettpriser = []
        for row in rows:
            billettpriser.append(BillettPris(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3])))
        return billettpriser
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, billettpris_list: List['BillettPris']) -> None:
        query = """
        INSERT INTO BillettPris (pris, billett_type, teaterstykket) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(billett_type, teaterstykket) DO NOTHING
        """
        values = [(billettpris.pris, billettpris.bilettType, billettpris.teaterstykket.id) for billettpris in billettpris_list]
        cursor.executemany(query, values)

class KundeProfil():
    def __init__(self, id: int, navn: str, adresse: str, telefon: str):
        self.id = id
        self.navn = navn
        self.adresse = adresse
        self.telefon = telefon

    def __str__(self):
        return f"KundeProfil(id={self.id}, navn={self.navn}, adresse={self.adresse}, telefon={self.telefon})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO KundeProfil (id, navn, adresse, telefon) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.navn, self.adresse, self.telefon))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM KundeProfil WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting KundeProfil: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE KundeProfil SET navn = ?, adresse = ?, telefon = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.adresse, self.telefon, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['KundeProfil']:
        query = "SELECT * FROM KundeProfil WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return KundeProfil(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['KundeProfil']:
        query = "SELECT * FROM KundeProfil"
        cursor.execute(query)
        rows = cursor.fetchall()
        kundeprofiler = []
        for row in rows:
            kundeprofiler.append(KundeProfil(row[0], row[1], row[2], row[3]))
        return kundeprofiler
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, kundeprofil_list: List['KundeProfil']) -> None:
        query = """
        INSERT INTO KundeProfil (navn, adresse, telefon) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(adresse) DO NOTHING
        """
        values = [(kundeprofil.navn, kundeprofil.adresse, kundeprofil.telefon) for kundeprofil in kundeprofil_list]
        cursor.executemany(query, values)

class BillettKjøp():
    id: int
    time: str
    dato: datetime.date
    kundeProfile: KundeProfil

    def __init__(self, id: int, time: str, dato: datetime.date, kundeProfile: KundeProfil):
        self.id = id
        self.time = time
        self.dato = dato
        self.kundeProfile = kundeProfile

    def __str__(self):
        return f"BillettKjøp(id={self.id}, time={self.time}, dato={self.dato}, kundeProfile={self.kundeProfile})"
    
    def insert(self, cursor: sqlite3.Cursor):
        query = "INSERT INTO BillettKjøp (id, tid, dato, kunde) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.id, self.time, self.dato, self.kundeProfile.id))
    
    def update(self):
        return f"UPDATE BillettKjøp SET time={self.time}, dato={self.dato}, kundeProfile={self.kundeProfile} WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM BillettKjøp WHERE id={self.id}"


class Billett():
    id: int
    visning: Visning
    stol: Stol
    billettPris: BillettPris
    billettKjøp: BillettKjøp

    def __init__(self, id: int, visning: Visning, stol: Stol, billettPris: BillettPris, billettKjøp: BillettKjøp):
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
    def __init__(self, id: int, nummer: int, teaterstykket: Teaterstykket, navn: str = None):
        self.id = id
        self.nummer = nummer
        self.navn = navn
        self.teaterstykket = teaterstykket

    def __str__(self):
        return f"Akt(id={self.id}, nummer={self.nummer}, navn={self.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Akt (id, nummer, navn, teaterstykket) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.nummer, self.navn, self.teaterstykket.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Akt WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Akt: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Akt SET nummer = ?, navn = ?, teaterstykket = ? WHERE id = ?"
        cursor.execute(query, (self.nummer, self.navn, self.teaterstykket.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Akt']:
        query = "SELECT * FROM Akt WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Akt(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_by_nummer_and_teaterstykket(cursor: sqlite3.Cursor, nummer: int, teaterstykket: Teaterstykket) -> Optional['Akt']:
        query = "SELECT * FROM Akt WHERE nummer = ? AND teaterstykket = ?"
        cursor.execute(query, (nummer, teaterstykket.id))
        row = cursor.fetchone()
        if row:
            return Akt(row[0], row[1], row[2], teaterstykket)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Akt']:
        query = "SELECT * FROM Akt"
        cursor.execute(query)
        rows = cursor.fetchall()
        aktene = []
        for row in rows:
            aktene.append(Akt(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3])))
        return aktene
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, akt_list: List['Akt']) -> None:
        query = """
        INSERT INTO Akt (nummer, navn, teaterstykket) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(nummer, teaterstykket) DO NOTHING
        """
        values = [(akt.nummer, akt.navn, akt.teaterstykket.id) for akt in akt_list]
        cursor.executemany(query, values)
        

class Skuespiller():
    id: int
    navn: str

    def __init__(self, id: int, navn: str):
        self.id = id
        self.navn = navn
    
    def __str__(self):
        return f"Skuespiller(id={self.id}, navn={self.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Skuespiller (id, navn) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.navn))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Skuespiller WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Skuespiller: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Skuespiller SET navn = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Skuespiller']:
        query = "SELECT * FROM Skuespiller WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Skuespiller(row[0], row[1])
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, navn: str) -> Optional['Skuespiller']:
        query = "SELECT * FROM Skuespiller WHERE navn = ?"
        cursor.execute(query, (navn,))
        row = cursor.fetchone()
        if row:
            return Skuespiller(row[0], row[1])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Skuespiller']:
        query = "SELECT * FROM Skuespiller"
        cursor.execute(query)
        rows = cursor.fetchall()
        skuespillere = []
        for row in rows:
            skuespillere.append(Skuespiller(row[0], row[1]))
        return skuespillere
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, skuespiller_list: List['Skuespiller']) -> None:
        query = """
        INSERT INTO Skuespiller (navn) VALUES (?)
        ON CONFLICT(id) DO NOTHING
        """
        values = [(skuespiller.navn,) for skuespiller in skuespiller_list]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_all_by_play(cursor: sqlite3.Cursor, teaterstykketId: int):
        query = """
        SELECT * FROM Skuespiller WHERE id = (
          SELECT (id) FROM SkuespillerRolleJunction WHERE rolle = (
            SELECT (id) FROM RolleAkterJunction WHERE akt = (
              SELECT (id) FROM Akt WHERE teaterstykket = ?
            )
          )
        )
        """
        cursor.execute(query, (teaterstykketId,))
        rows = cursor.fetchall()
        actors = []
        if rows:
            for row in rows:
                actors.append(Skuespiller(row[0], row[1]))
            return actors
        return None



    
class Roller():
    id: int
    navn: str

    def __init__(self, id: int, navn: str):
        self.id = id
        self.navn = navn

    def __str__(self):
        return f"Roller(id={self.id}, navn={self.navn})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Roller (id, navn) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.navn))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Roller WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Roller: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Roller SET navn = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Roller']:
        query = "SELECT * FROM Roller WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Roller(row[0], row[1])
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, navn: str) -> Optional['Roller']:
        query = "SELECT * FROM Roller WHERE navn = ?"
        cursor.execute(query, (navn,))
        row = cursor.fetchone()
        if row:
            return Roller(row[0], row[1])
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Roller']:
        query = "SELECT * FROM Roller"
        cursor.execute(query)
        rows = cursor.fetchall()
        roller = []
        for row in rows:
            roller.append(Roller(row[0], row[1]))
        return roller
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, roller_list: List['Roller']) -> None:
        query = """
        INSERT INTO Roller (navn) VALUES (?)
        ON CONFLICT(id) DO NOTHING
        """
        values = [(roller.navn,) for roller in roller_list]
        cursor.executemany(query, values)
    

class RolleAkterJunction():
    def __init__(self, akt: Akt, rolle: Roller):
        self.akt = akt
        self.rolle = rolle

    def __str__(self):
        return f"RolleAkterJunction(akt={self.akt}, rolle={self.rolle})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO RolleAkterJunction (akt, rolle) VALUES (?, ?)
        ON CONFLICT(akt, rolle) DO NOTHING  
        """
        cursor.execute(query, (self.akt.id, self.rolle.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM RolleAkterJunction WHERE akt = ? AND rolle = ?"
            cursor.execute(query, (self.akt.id, self.rolle.id))
            return True
        except Exception as e:
            print(f"Error deleting RolleAkterJunction: {e}")
            return False
        
    @staticmethod
    def get_by_akt(cursor: sqlite3.Cursor, akt: Akt) -> List['RolleAkterJunction']:
        query = "SELECT * FROM RolleAkterJunction WHERE akt = ?"
        cursor.execute(query, (akt.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RolleAkterJunction(akt, Roller.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_rolle(cursor: sqlite3.Cursor, rolle: Roller) -> List['RolleAkterJunction']:
        query = "SELECT * FROM RolleAkterJunction WHERE rolle = ?"
        cursor.execute(query, (rolle.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RolleAkterJunction(Akt.get_by_id(cursor, row[0]), rolle))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['RolleAkterJunction']:
        query = "SELECT * FROM RolleAktJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RolleAkterJunction(Akt.get_by_id(cursor, row[0]), Roller.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['RolleAkterJunction']) -> None:
        query = """
        INSERT INTO RolleAkterJunction (akt, rolle) VALUES (?, ?)
        ON CONFLICT(akt, rolle) DO NOTHING
        """
        values = [(junction.akt.id, junction.rolle.id) for junction in junction_list]
        cursor.executemany(query, values)
        
    

class SkuespillerRolleJunction():
    def __init__(self, skuespiller: Skuespiller, rolle: Roller):
        self.skuespiller = skuespiller
        self.rolle = rolle

    def __str__(self):
        return f"SkuespillerRolleJunction(skuespiller={self.skuespiller}, rolle={self.rolle})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO SkuespillerRolleJunction (skuespiller, rolle) VALUES (?, ?)
        ON CONFLICT(skuespiller, rolle) DO NOTHING
        """
        cursor.execute(query, (self.skuespiller.id, self.rolle.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM SkuespillerRolleJunction WHERE skuespiller = ? AND rolle = ?"
            cursor.execute(query, (self.skuespiller.id, self.rolle.id))
            return True
        except Exception as e:
            print(f"Error deleting SkuespillerRolleJunction: {e}")
            return False
        
    @staticmethod
    def get_by_skuespiller(cursor: sqlite3.Cursor, skuespiller: Skuespiller) -> List['SkuespillerRolleJunction']:
        query = "SELECT * FROM SkuespillerRolleJunction WHERE skuespiller = ?"
        cursor.execute(query, (skuespiller.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerRolleJunction(skuespiller, Roller.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_rolle(cursor: sqlite3.Cursor, rolle: Roller) -> List['SkuespillerRolleJunction']:
        query = "SELECT * FROM SkuespillerRolleJunction WHERE rolle = ?"
        cursor.execute(query, (rolle.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerRolleJunction(Skuespiller.get_by_id(cursor, row[0]), rolle))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['SkuespillerRolleJunction']:
        query = "SELECT * FROM SkuespillerRolleJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerRolleJunction(Skuespiller.get_by_id(cursor, row[0]), Roller.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['SkuespillerRolleJunction']) -> None:
        query = """
        INSERT INTO SkuespillerRolleJunction (skuespiller, rolle) VALUES (?, ?)
        ON CONFLICT(skuespiller, rolle) DO NOTHING
        """
        values = [(junction.skuespiller.id, junction.rolle.id) for junction in junction_list]
        cursor.executemany(query, values)

class Oppgave():
    def __init__(self, id: int, navn: str, beskrivelse: str, teaterstykket: Teaterstykket):
        self.id = id
        self.navn = navn
        self.beskrivelse = beskrivelse
        self.teaterstykket = teaterstykket

    def __str__(self):
        return f"Oppgave(id={self.id}, navn={self.navn}, beskrivelse={self.beskrivelse}, teaterstykket={self.teaterstykket})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Oppgave (id, navn, beskrivelse, teaterstykket) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.navn, self.beskrivelse, self.teaterstykket.id))

    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Oppgave WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Oppgave: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Oppgave SET navn = ?, beskrivelse = ?, teaterstykket = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.beskrivelse, self.teaterstykket.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Oppgave']:
        query = "SELECT * FROM Oppgave WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Oppgave(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Oppgave']:
        query = "SELECT * FROM Oppgave"
        cursor.execute(query)
        rows = cursor.fetchall()
        oppgaver = []
        for row in rows:
            oppgaver.append(Oppgave(row[0], row[1], row[2], Teaterstykket.get_by_id(cursor, row[3])))
        return oppgaver
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, oppgave_list: List['Oppgave']) -> None:
        query = """
        INSERT INTO Oppgave (navn, beskrivelse, teaterstykket) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(navn, teaterstykket) DO NOTHING
        """
        values = [(oppgave.navn, oppgave.beskrivelse, oppgave.teaterstykket.id) for oppgave in oppgave_list]
        cursor.executemany(query, values)


class AnsattStatus():
    def __init__(self, status: str):
        self.status = status

    def __str__(self):
        return f"AnsattStatus(status={self.status})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO AnsattStatus (status) VALUES (?)
        ON CONFLICT(status) DO NOTHING
        """
        cursor.execute(query, (self.status,))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM AnsattStatus WHERE status = ?"
            cursor.execute(query, (self.status,))
            return True
        except Exception as e:
            print(f"Error deleting AnsattStatus: {e}")
            return False

    @staticmethod
    def get_by_status(cursor: sqlite3.Cursor, status: str) -> Optional['AnsattStatus']:
        query = "SELECT * FROM AnsattStatus WHERE status = ?"
        cursor.execute(query, (status,))
        row = cursor.fetchone()
        if row:
            return AnsattStatus(row[0])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['AnsattStatus']:
        query = "SELECT * FROM AnsattStatus"
        cursor.execute(query)
        rows = cursor.fetchall()
        statusene = []
        for row in rows:
            statusene.append(AnsattStatus(row[0]))
        return statusene
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, status_list: List['AnsattStatus']) -> None:
        query = """
        INSERT INTO AnsattStatus (status) VALUES (?)
        ON CONFLICT(status) DO NOTHING
        """
        values = [(status.status,) for status in status_list]
        cursor.executemany(query, values)

class StillingsTittel():
    def __init__(self, tittel: str):
        self.tittel = tittel

    def __str__(self):
        return f"StillingsTittel(tittel={self.tittel})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO StillingsTittel (tittel) VALUES (?)
        ON CONFLICT(tittel) DO NOTHING
        """
        cursor.execute(query, (self.tittel,))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM StillingsTittel WHERE tittel = ?"
            cursor.execute(query, (self.tittel,))
            return True
        except Exception as e:
            print(f"Error deleting StillingsTittel: {e}")
            return False
        
    @staticmethod
    def get_by_tittel(cursor: sqlite3.Cursor, tittel: str) -> Optional['StillingsTittel']:
        query = "SELECT * FROM StillingsTittel WHERE tittel = ?"
        cursor.execute(query, (tittel,))
        row = cursor.fetchone()
        if row:
            return StillingsTittel(row[0])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['StillingsTittel']:
        query = "SELECT * FROM StillingsTittel"
        cursor.execute(query)
        rows = cursor.fetchall()
        titlene = []
        for row in rows:
            titlene.append(StillingsTittel(row[0]))
        return titlene

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, tittel_list: List['StillingsTittel']) -> None:
        query = """
        INSERT INTO StillingsTittel (tittel) VALUES (?)
        ON CONFLICT(tittel) DO NOTHING
        """
        values = [(tittel.tittel,) for tittel in tittel_list]
        cursor.executemany(query, values)        

class Medvirkende():
    def __init__(self, id: int, navn: str, email: str, status: AnsattStatus, stilling: StillingsTittel=None):
        self.id = id
        self.navn = navn
        self.email = email
        self.status = status
        self.stilling = stilling

    def __str__(self):
        return f"Medvirkende(id={self.id}, navn={self.navn}, email={self.email}, status={self.status}, stilling={self.stilling})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Medvirkende (id, navn, email, status, stilling) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(email) DO NOTHING
        """
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Medvirkende WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Medvirkende: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Medvirkende SET navn = ?, email = ?, status = ?, stilling = ? WHERE id = ?"
        cursor.execute(query, (self.navn, self.email, self.status.status, self.stilling.tittel if self.stilling else None, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Medvirkende']:
        query = "SELECT * FROM Medvirkende WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            status = AnsattStatus(row[3])
            stilling = StillingsTittel(row[4]) if row[4] else None
            return Medvirkende(row[0], row[1], row[2], status, stilling)
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Medvirkende']:
        query = "SELECT * FROM Medvirkende"
        cursor.execute(query)
        rows = cursor.fetchall()
        medvirkende = []
        for row in rows:
            status = AnsattStatus(row[3])
            stilling = StillingsTittel(row[4]) if row[4] else None
            medvirkende.append(Medvirkende(row[0], row[1], row[2], status, stilling))
        return medvirkende
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, medvirkende_list: List['Medvirkende']) -> None:
        query = """
        INSERT INTO Medvirkende (navn, email, status, stilling) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(email) DO NOTHING
        """
        values = [(medvirkende.navn, medvirkende.email, medvirkende.status.status, medvirkende.stilling.tittel if medvirkende.stilling else None) for medvirkende in medvirkende_list]
        cursor.executemany(query, values)


class SkuespillerOppgaveJunction():
    skuespiller: Skuespiller
    oppgave: Oppgave

    def __init__(self, skuespiller: Skuespiller, oppgave: Oppgave):
        self.skuespiller = skuespiller
        self.oppgave = oppgave

    def __str__(self):
        return f"SkuespillerOppgaveJunction(skuespiller={self.skuespiller}, oppgave={self.oppgave})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO SkuespillerOppgaveJunction (skuespiller, oppgave) VALUES (?, ?)
        ON CONFLICT(skuespiller, oppgave) DO NOTHING
        """
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM SkuespillerOppgaveJunction WHERE skuespiller = ? AND oppgave = ?"
            cursor.execute(query, (self.skuespiller.id, self.oppgave.id))
            return True
        except Exception as e:
            print(f"Error deleting SkuespillerOppgaveJunction: {e}")
            return False
        
    @staticmethod
    def get_by_skuespiller(cursor: sqlite3.Cursor, skuespiller: Skuespiller) -> List['SkuespillerOppgaveJunction']:
        query = "SELECT * FROM SkuespillerOppgaveJunction WHERE skuespiller = ?"
        cursor.execute(query, (skuespiller.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerOppgaveJunction(skuespiller, Oppgave.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_oppgave(cursor: sqlite3.Cursor, oppgave: Oppgave) -> List['SkuespillerOppgaveJunction']:
        query = "SELECT * FROM SkuespillerOppgaveJunction WHERE oppgave = ?"
        cursor.execute(query, (oppgave.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerOppgaveJunction(Skuespiller.get_by_id(cursor, row[0]), oppgave))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['SkuespillerOppgaveJunction']:
        query = "SELECT * FROM SkuespillerOppgaveJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(SkuespillerOppgaveJunction(Skuespiller.get_by_id(cursor, row[0]), Oppgave.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['SkuespillerOppgaveJunction']) -> None:
        query = """
        INSERT INTO SkuespillerOppgaveJunction (skuespiller, oppgave) VALUES (?, ?)
        ON CONFLICT(skuespiller, oppgave) DO NOTHING
        """
        values = [(junction.skuespiller.id, junction.oppgave.id) for junction in junction_list]
        cursor.executemany(query, values)
