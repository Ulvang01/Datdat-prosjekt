CREATE TABLE Sal (
    navn VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Område (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL,
    sal VARCHAR(255) NOT NULL,
    FOREIGN KEY (sal) REFERENCES Sal(navn),
    UNIQUE (navn, sal)
);

CREATE TABLE Rad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    radnr INTEGER NOT NULL,
    område INTEGER NOT NULL,
    FOREIGN KEY (område) REFERENCES Område(id),
    UNIQUE (radnr, område)
);

CREATE TABLE Stol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stol_nr INTEGER NOT NULL,
    rad INTEGER NOT NULL,
    UNIQUE (stol_nr, rad),
    FOREIGN KEY (rad) REFERENCES Rad(id)
);

CREATE TABLE Teaterstykket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL,
    forfatter VARCHAR(255) NOT NULL,
    sal VARCHAR(255) NOT NULL,
    tid TIME NOT NULL,
    FOREIGN KEY (sal) REFERENCES Sal(navn),
    UNIQUE (navn, forfatter)
);

CREATE TABLE Visning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dato DATE NOT NULL,
    teaterstykket INTEGER NOT NULL,
    FOREIGN KEY (teaterstykket) REFERENCES Teaterstykket(id),
    UNIQUE (dato, teaterstykket)
);

CREATE TABLE Kundeprofil (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL,
    telefon INTEGER NOT NULL UNIQUE,
    adresse VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE BilletKjøp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunde INTEGER NOT NULL,
    dato DATE NOT NULL,
    tid TIME NOT NULL,
    FOREIGN KEY (kunde) REFERENCES Kundeprofil(id)
);

CREATE TABLE BillettPris (
    id INTEGER PRIMARY KEY,
    billett_type VARCHAR(255) NOT NULL,
    teaterstykket INTEGER NOT NULL,
    pris INTEGER NOT NULL,
    FOREIGN KEY (teaterstykket) REFERENCES Teaterstykket(id),
    UNIQUE (billett_type, teaterstykket)
);

CREATE TABLE Billett (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vising INTEGER NOT NULL,
    sete INTEGER NOT NULL,
    kjøp INTEGER NOT NULL,
    pris INTEGER NOT NULL,
    FOREIGN KEY (vising) REFERENCES Visning(id),
    FOREIGN KEY (sete) REFERENCES Stol(id),
    FOREIGN KEY (kjøp) REFERENCES BilletKjøp(id),
    FOREIGN KEY (pris) REFERENCES BillettPris(id),
    UNIQUE (vising, sete, kjøp, pris)
);

CREATE TABLE Skuespiller (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL
);

CREATE TABLE Roller (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL
);

CREATE TABLE SkuespillerRolleJunction (
    skuespiller INTEGER NOT NULL,
    rolle INTEGER NOT NULL,
    PRIMARY KEY (skuespiller, rolle),
    FOREIGN KEY (skuespiller) REFERENCES Skuespiller(id),
    FOREIGN KEY (rolle) REFERENCES Roller(id)
);

CREATE TABLE Akt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nummer INTEGER NOT NULL,
    navn VARCHAR(255),
    teaterstykket INTEGER NOT NULL,
    FOREIGN KEY (teaterstykket) REFERENCES Teaterstykket(id),
    UNIQUE (nummer, teaterstykket)
);

CREATE TABLE RolleAkterJunction (
    rolle INTEGER NOT NULL,
    akt INTEGER NOT NULL,
    PRIMARY KEY (rolle, akt),
    FOREIGN KEY (rolle) REFERENCES Roller(id),
    FOREIGN KEY (akt) REFERENCES Akt(id)
);

CREATE TABLE Medvirkende (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    ansatt_status VARCHAR(255) NOT NULL,
    stillings_tittel VARCHAR(255) NOT NULL,
    FOREIGN KEY (ansatt_status) REFERENCES AnsattStatus(ansatt_status),
    FOREIGN KEY (stillings_tittel) REFERENCES StillingsTittel(stillings_tittel)
);

CREATE TABLE AnsattStatus (
    ansatt_status VARCHAR(255) PRIMARY KEY
);

CREATE TABLE StillingsTittel (
    stillings_tittel VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Oppgave (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navn VARCHAR(255) NOT NULL,
    beskrivelse VARCHAR(255) NOT NULL,
    teaterstykket INTEGER NOT NULL,
    FOREIGN KEY (teaterstykket) REFERENCES Teaterstykket(id)
);

CREATE TABLE OppgaveMedvirkendeJunctoin (
    oppgave INTEGER NOT NULL,
    medvirkende INTEGER NOT NULL,
    PRIMARY KEY (oppgave, medvirkende),
    FOREIGN KEY (oppgave) REFERENCES Oppgave(id),
    FOREIGN KEY (medvirkende) REFERENCES Medvirkende(id)
);
