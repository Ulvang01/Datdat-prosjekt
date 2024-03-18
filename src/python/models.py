import datetime

class Sal():
    navn: str

    def __init__(self, navn: str):
        self.navn = navn

    def __str__(self):
        return f"Sal(navn={self.navn})"
    
    def insert(self):
        return f"INSERT INTO Sal (navn) VALUES ('{self.navn}')"
    
    def delete(self):
        return f"DELETE FROM Sal WHERE navn='{self.navn}'"
    
    def get(self):
        return f"SELECT * FROM Sal WHERE navn='{self.navn}'"

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


class Område():
    id: int
    navn: str
    sal: Sal

    def __init__(self, id: int, navn: str, sal: Sal):
        self.id = id
        self.navn = navn
        self.sal = sal

    def __str__(self):
        return f"Område(id={self.id}, navn={self.navn}, sal={self.sal})"
    
    def insert(self):
        return f"INSERT INTO Område (id, navn, sal) VALUES ('{self.id}', '{self.navn}', '{self.sal.navn}')"
    
    def update(self):
        return f"UPDATE Område SET navn='{self.navn}', sal='{self.sal.navn}' WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Område WHERE id='{self.id}'"
    
    def get(self, id: int):
        return f"SELECT * FROM Område WHERE id='{id}'"
    
    @staticmethod
    def get_all():
        return f"SELECT * FROM Område"
    
    @staticmethod
    def get_by_sal(sal: str):
        return f"SELECT * FROM Område WHERE sal='{sal}'"

class Rad():
    id: int
    radnr: int
    område: Område

    def __init__(self, id: int, radnr: int, område: Område):
        self.id = id
        self.radnr = radnr
        self.område = område

    def __str__(self):
        return f"Rad(id={self.id}, radnr={self.radnr}, område={self.område})"
    
    def insert(self):
        return f"INSERT INTO Rad (id, radnr, område) VALUES ('{self.id}', '{self.radnr}', '{self.område}')"
    
    def update(self):
        return f"UPDATE Rad SET radnr='{self.radnr}', område='{self.område}' WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Rad WHERE id='{self.id}'"
    
    def get(self, id: int):
        return f"SELECT * FROM Rad WHERE id='{id}'"
    
    @staticmethod
    def get_all():
        return f"SELECT * FROM Rad"

class Stol():
    id: int
    stolnr: int
    rad: Rad

    def __init__(self, id: int, stolnr: int, rad: Rad):
        self.id = id
        self.stolnr = stolnr
        self.rad = rad

    def __str__(self):
        return f"Stol(id={self.id}, stolnr={self.stolnr}, rad={self.rad.id})"
    
    def insert(self):
        return f"INSERT INTO Stol (id, stol_nr, rad) VALUES ('{self.id}', '{self.stolnr}', '{self.rad.id}')"
    
    def update(self):
        return f"UPDATE Stol SET stol_nr='{self.stolnr}', rad='{self.rad.id}' WHERE id={self.id}"
    
    def delete(self):
        return f"DELETE FROM Stol WHERE id='{self.id}'"
    
    def get(self, id: int):
        return f"SELECT * FROM Stol WHERE id='{id}'"

    @staticmethod
    def get_all():
        return f"SELECT * FROM Stol"

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
    
