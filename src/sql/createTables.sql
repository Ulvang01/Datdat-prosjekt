CREATE TABLE Scene (
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    scene VARCHAR(255) NOT NULL,
    FOREIGN KEY (scene) REFERENCES Scene(name),
    UNIQUE (name, scene)
);

CREATE TABLE Row (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    row_num INTEGER NOT NULL,
    area INTEGER NOT NULL,
    FOREIGN KEY (area) REFERENCES Area(id),
    UNIQUE (row_num, area)
);

CREATE TABLE Chair (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chair_num INTEGER NOT NULL,
    row INTEGER NOT NULL,
    UNIQUE (chair_num, row),
    FOREIGN KEY (row) REFERENCES Row(id)
);

CREATE TABLE Play (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    scene VARCHAR(255) NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (scene) REFERENCES Scene(name),
    UNIQUE (name, author)
);

CREATE TABLE Screening (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    play INTEGER NOT NULL,
    FOREIGN KEY (play) REFERENCES Play(id),
    UNIQUE (date, play)
);

CREATE TABLE CustomerProfile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    telephone_num INTEGER NOT NULL UNIQUE,
    adress VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE TicketPurchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer INTEGER NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (customer) REFERENCES CustomerProfile(id)
);

CREATE TABLE TicketPrice (
    id INTEGER PRIMARY KEY,
    ticket_type VARCHAR(255) NOT NULL,
    play INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (play) REFERENCES Play(id),
    UNIQUE (ticket_type, play)
);

CREATE TABLE Ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screening INTEGER NOT NULL,
    chair INTEGER NOT NULL,
    purchase INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (screening) REFERENCES Screening(id),
    FOREIGN KEY (chair) REFERENCES Stol(id),
    FOREIGN KEY (purchase) REFERENCES BilletKjøp(id),
    FOREIGN KEY (price) REFERENCES TicketPrice(id),
    UNIQUE (screening, chair, purchase, price)
);

CREATE TABLE Actor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE SkuespillerRolleJunction (
    actor INTEGER NOT NULL,
    role INTEGER NOT NULL,
    PRIMARY KEY (actor, role),
    FOREIGN KEY (actor) REFERENCES Actor(id),
    FOREIGN KEY (role) REFERENCES Role(id)
);

CREATE TABLE Akt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL,
    name VARCHAR(255),
    play INTEGER NOT NULL,
    FOREIGN KEY (play) REFERENCES Play(id),
    UNIQUE (number, play)
);

CREATE TABLE RoleActJunction (
    role INTEGER NOT NULL,
    act INTEGER NOT NULL,
    PRIMARY KEY (role, act),
    FOREIGN KEY (role) REFERENCES Role(id),
    FOREIGN KEY (act) REFERENCES Akt(id)
);

CREATE TABLE Contributor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    employee_status VARCHAR(255) NOT NULL,
    FOREIGN KEY (employee_status) REFERENCES AnsattStatus(employee_status)
);

CREATE TABLE EmployeeStatus (
    employee_status VARCHAR(255) PRIMARY KEY
);


CREATE TABLE Task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    play INTEGER NOT NULL,
    FOREIGN KEY (play) REFERENCES Play(id)
);

CREATE TABLE TaskContributorJunction (
    task INTEGER NOT NULL,
    contributor INTEGER NOT NULL,
    PRIMARY KEY (task, contributor),
    FOREIGN KEY (task) REFERENCES Oppgave(id),
    FOREIGN KEY (contributor) REFERENCES Contributor(id)
);
