import datetime
import sqlite3
from typing import List, Optional, Tuple

class Scene:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Scene(name={self.name})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Scene (name) VALUES (?)
        ON CONFLICT(name) DO NOTHING
        """
        cursor.execute(query, (self.name,))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Scene WHERE name=?"
            cursor.execute(query, (self.name,))
            return True
        except Exception as e:
            print(f"Error deleting Scene: {e}")
            return False

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Scene']:
        cursor.execute("SELECT * FROM Scene")
        return [Scene(row[0]) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str) -> Optional['Scene']:
        query = "SELECT * FROM Scene WHERE name=?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            return Scene(row[0])
        return None


class Area:
    def __init__(self, id: int, name: str, scene: Scene):
        self.id = id
        self.name = name
        self.scene = scene

    def __repr__(self) -> str:
        return f"Area(id={self.id}, name={self.name}, scene={self.scene.name})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Area (name, scene) VALUES (?, ?)
        ON CONFLICT(name, scene) DO NOTHING
        """
        cursor.execute(query, (self.name, self.scene.name))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Area WHERE name=? AND scene=?"
            cursor.execute(query, (self.name, self.scene.name))
            return True
        except Exception as e:
            print(f"Error deleting Area: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Area SET name=?, scene=? WHERE id=?"
        cursor.execute(query, (self.name, self.scene.name, self.id))
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, arear: List['Area']) -> None:
        query = """
        INSERT INTO Area (name, scene) VALUES (?, ?)
        ON CONFLICT(name, scene) DO NOTHING
        """
        values = [(area.name, area.scene.name) for area in arear]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Area']:
        query = "SELECT * FROM Area"
        cursor.execute(query)
        return [Area(row[0], row[1], Scene.get_by_name(row[2])) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_scene(cursor: sqlite3.Cursor, scene: Scene) -> List['Area']:
        query = "SELECT * FROM Area WHERE scene=?"
        cursor.execute(query, (scene.name,))
        return [Area(row[0], row[1], scene) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Area']:
        query = "SELECT * FROM Area WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            scene = Scene.get_by_name(cursor, row[2])
            if scene:
                return Area(row[0], row[1], scene)
        return None

class Row:
    def __init__(self, id: int, row_num: int, area: Area):
        self.id = id
        self.row_num = row_num
        self.area = area

    def __str__(self) -> str:
        return f"Row(id={self.id}, row_num={self.row_num}, area={self.area.id})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Row (id, row_num, area) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.row_num, self.area.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Row WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Row: {e}")
            return False
    
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Row SET row_num = ?, area = ? WHERE id = ?"
        cursor.execute(query, (self.row_num, self.area.id, self.id))
    
    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Row']:
        query = "SELECT * FROM Row WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            area = Area.get_by_id(cursor, row[2])
            if area:
                return Row(row[0], row[1], area)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Row']:
        query = "SELECT * FROM Row"
        cursor.execute(query)
        rows = cursor.fetchall()
        rows = []
        for row in rows:
            area = Area.get_by_id(cursor, row[2])
            if area:
                rows.append(Row(row[0], row[1], area))
        return rows
    
    @staticmethod
    def get_by_area_and_row_num(cursor: sqlite3.Cursor, area: Area, row_num: int) -> List['Row']:
        query = "SELECT * FROM Row WHERE area = ? AND row_num = ?"
        cursor.execute(query, (area.id, row_num))
        rows = cursor.fetchone()
        row = Row(rows[0], row_num, area)
        return row
    
    @staticmethod
    def get_by_scene(cursor: sqlite3.Cursor, scene: Scene) -> List['Row']:
        query = "SELECT * FROM Row WHERE area IN (SELECT id FROM Area WHERE scene = ?)"
        cursor.execute(query, (scene.name,))
        rows = cursor.fetchall()
        rows = []
        for row in rows:
            area = Area.get_by_id(cursor, row[2])
            if area:
                rows.append(Row(row[0], row[1], area))
        return rows

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, row_list: List['Row']) -> None:
        query = """
        INSERT INTO Row (row_num, area) VALUES ( ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(row_num, area) DO NOTHING
        """
        values = [(row.row_num, row.area.id) for row in row_list]
        cursor.executemany(query, values)

class Chair:
    def __init__(self, id: int, chair_num: int, row: Row):
        self.id = id
        self.chair_num = chair_num
        self.row = row

    def __str__(self) -> str:
        return f"Chair(id={self.id}, chair_num={self.chair_num}, row={self.row.id})"

    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = "INSERT INTO Chair (id, chair_num, row) VALUES (?, ?, ?)"
        cursor.execute(query, (self.id, self.chair_num, self.row.id))

    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Chair SET chair_num = ?, row = ? WHERE id = ?"
        cursor.execute(query, (self.chair_num, self.row.id, self.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Chair WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Chair: {e}")
            return False

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Chair']:
        query = "SELECT * FROM Chair WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            chair_row = Row.get_by_id(cursor, row[2]) 
            if row:
                return Chair(row[0], row[1], chair_row)
        return None
    
    @staticmethod
    def get_by_row_and_num(cursor: sqlite3.Cursor, row: Row, chair_num: int) -> Optional['Chair']:
        query = "SELECT * FROM Chair WHERE row = ? AND chair_num = ?"
        cursor.execute(query, (row.id, chair_num))
        row = cursor.fetchone()
        if row:
            chari_row = Row.get_by_id(cursor, row[2])
            if row:
                return Chair(row[0], row[1], chari_row)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Chair']:
        query = "SELECT * FROM Chair"
        cursor.execute(query)
        rows = cursor.fetchall()
        chairs = []
        for row in rows:
            row = Row.get_by_id(cursor, row[2])
            if row:
                chairs.append(Chair(row[0], row[1], row))
        return chairs
    
    @staticmethod
    def get_by_scene(cursor: sqlite3.Cursor, scene: Scene) -> List['Chair']:
        query = "SELECT * FROM Chair WHERE row IN (SELECT id FROM Row WHERE area IN (SELECT id FROM Area WHERE scene = ?))"
        cursor.execute(query, (scene.name,))
        rows = cursor.fetchall()
        chairs = []
        for row in rows:
            chairs_row = Row.get_by_id(cursor, row[2])
            if chairs_row:
                chairs.append(Chair(row[0], row[1], chairs_row))
        return chairs

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, chair_list: List['Chair']) -> None:
        query = """
        INSERT INTO Chair (chair_num, row) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(chair_num, row) DO NOTHING
        """
        values = [(chair.chair_num, chair.row.id) for chair in chair_list]
        cursor.executemany(query, values)

class Play():
    def __init__(self, id: int, name: str, author: str, time: str, scene: Scene):
        self.id = id
        self.name = name
        self.author = author
        self.time = time
        self.scene = scene
    
    def __str__(self):
        return f"play(id={self.id}, name={self.name}, author={self.author}, time={self.time})"

    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Play (id, name, author, time, scene) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name, self.author, self.time, self.scene.name))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Play WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Play: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Play SET name = ?, author = ?, time = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.author, self.time, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Play']:
        query = "SELECT * FROM Play WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Play(id, row[1], row[2], row[4], row[3])
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str) -> Optional['Play']:
        query = "SELECT * FROM Play WHERE name = ?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            return Play(int(row[0]), row[1], row[2], row[4], row[3])
        return None
    
    def get_by_scene(cursor: sqlite3.Cursor, scene: Scene) -> Optional['Play']:
        query = "SELECT * FROM Play WHERE scene = ?"
        cursor.execute(query, (scene.name,))
        row = cursor.fetchone()
        play = Play(row[0], row[1], row[2], row[4], row[3])
        return play

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Play']:
        query = "SELECT * FROM Play"
        cursor.execute(query)
        rows = cursor.fetchall()
        plays = []
        for row in rows:
            plays.append(Play(int(row[0]), row[1], row[2], row[4], row[3]))
        return plays
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, play_list: List['Play']) -> None:
        query = """
        INSERT INTO Play (name, author, time) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(name, author) DO NOTHING
        """
        values = [(play.name, play.author, play.time) for play in play_list]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str):
        query = """
        SELECT * FROM Play WHERE name = ?
        """
        cursor.execute(query, (name,))
        play = cursor.fetchone()
        if play:
            return Play(play[0], play[1], play[2], play[3], play[4])
        return None
    
    @staticmethod
    def get_plays_on_date(cursor: sqlite3.Cursor, date: str):
        query = """
        SELECT * FROM Play WHERE id = (
          SELECT (play) from Screening WHERE date = ?
        )
        """
        cursor.execute(query, (date,))
        rows = cursor.fetchall()
        plays = []
        if rows:
            for row in rows:
                plays.append(Play(row[0], row[1], row[2], row[3], row[4]))
            return plays
        return None


class Screening():
    id: int
    date: datetime.date
    play: Play

    def __init__(self, id: int, date: datetime.date, play: Play):
        self.id = id
        self.date = date
        self.play = play

    def __str__(self):
        return f"Screening(id={self.id}, date={self.date}, play={self.play})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Screening (id, date, play) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.date, self.play.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Screening WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Screening: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Screening SET date = ?, play = ? WHERE id = ?"
        cursor.execute(query, (self.date, self.play.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Screening']:
        query = "SELECT * FROM Screening WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Screening(row[0], row[1], Play.get_by_id(cursor, row[2]))
        return None
    
    @staticmethod
    def get_by_date_and_play(cursor: sqlite3.Cursor, date: datetime.date, play: Play) -> Optional['Screening']:
        query = "SELECT * FROM Screening WHERE date = ? AND play = ?"
        cursor.execute(query, (date, play.id))
        row = cursor.fetchone()
        if row:
            return Screening(row[0], row[1], play)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Screening']:
        query = "SELECT * FROM Screening"
        cursor.execute(query)
        rows = cursor.fetchall()
        screenings = []
        for row in rows:
            screenings.append(Screening(row[0], row[1], Play.get_by_id(cursor, row[2])))
        return screenings
    
    @staticmethod
    def get_bestselling(cursor: sqlite3.Cursor) -> Optional[Tuple['Screening', int]]:
        query = """
        SELECT screening, COUNT(*) AS screeningCount
        FROM Ticket
        GROUP BY screening
        ORDER BY screeningCount DESC
        LIMIT 1;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return [Screening.get_by_id(cursor, row[0]), row[1]]
        return None

    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, screening_list: List['Screening']) -> None:
        query = """
        INSERT INTO Screening (date, play) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(date, play) DO NOTHING
        """
        values = [(screening.date, screening.play.id) for screening in screening_list]
        cursor.executemany(query, values)

class TicketPrice():
    def __init__(self, id: int, price: float, ticket_type: str, play: Play):
        self.id = id
        self.price = price
        self.ticket_type = ticket_type
        self.play = play

    def __str__(self):
        return f"TicketPrice(id={self.id}, price={self.price}, ticket_type={self.ticket_type}, play={self.play})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO TicketPrice (id, price, ticket_type, play) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.price, self.ticket_type, self.play.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM TicketPrice WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting TicketPrice: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE TicketPrice SET price = ?, ticket_type = ?, play = ? WHERE id = ?"
        cursor.execute(query, (self.price, self.ticket_type, self.play.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['TicketPrice']:
        query = "SELECT * FROM TicketPrice WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return TicketPrice(row[0], row[3], row[1], Play.get_by_id(cursor, row[2]))
        return None
    
    @staticmethod
    def get_by_play_and_type(cursor: sqlite3.Cursor, play: Play, ticket_type: str) -> Optional['TicketPrice']:
        query = "SELECT * FROM TicketPrice WHERE play = ? AND ticket_type = ?"
        values = (play.id, ticket_type)
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row:
            return TicketPrice(row[0], row[3], row[1], Play.get_by_id(cursor, row[2]))
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['TicketPrice']:
        query = "SELECT * FROM TicketPrice"
        cursor.execute(query)
        rows = cursor.fetchall()
        ticketprices = []
        for row in rows:
            ticketprices.append(TicketPrice(row[0], row[1], row[2], Play.get_by_id(cursor, row[3])))
        return ticketprices
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, ticketprice_list: List['TicketPrice']) -> None:
        query = """
        INSERT INTO TicketPrice (price, ticket_type, play) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(ticket_type, play) DO NOTHING
        """
        values = [(ticketpirce.price, ticketpirce.ticket_type, ticketpirce.play.id) for ticketpirce in ticketprice_list]
        cursor.executemany(query, values)

class CustomerProfile():
    def __init__(self, id: int, name: str, adress: str, telephone_num: str):
        self.id = id
        self.name = name
        self.adress = adress
        self.telephone_num = telephone_num

    def __str__(self):
        return f"CustomerProfile(id={self.id}, name={self.name}, adress={self.adress}, telephone_num={self.telephone_num})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO CustomerProfile (id, name, adress, telephone_num) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(adress) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name, self.adress, self.telephone_num))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM CustomerProfile WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting CustomerProfile: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE CustomerProfile SET name = ?, adress = ?, telephone_num = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.adress, self.telephone_num, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['CustomerProfile']:
        query = "SELECT * FROM CustomerProfile WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return CustomerProfile(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def get_by_name_and_address(cursor: sqlite3.Cursor, name: str, adress: str) -> Optional['CustomerProfile']:
        query = "SELECT * FROM CustomerProfile WHERE name = ? AND adress = ?"
        cursor.execute(query, (name, adress))
        row = cursor.fetchone()
        if row:
            return CustomerProfile(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['CustomerProfile']:
        query = "SELECT * FROM CustomerProfile"
        cursor.execute(query)
        rows = cursor.fetchall()
        customerprofiles = []
        for row in rows:
            customerprofiles.append(CustomerProfile(row[0], row[1], row[2], row[3]))
        return customerprofiles
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, customerprofile_list: List['CustomerProfile']) -> None:
        query = """
        INSERT INTO CustomerProfile (name, adress, telephone_num) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(adress) DO NOTHING
        """
        values = [(customerprofile.name, customerprofile.adress, customerprofile.telephone_num) for customerprofile in customerprofile_list]
        cursor.executemany(query, values)

class TicketPurchase():
    def __init__(self, id: int, time: str, date: datetime.date, customer: CustomerProfile):
        self.id = id
        self.time = time
        self.date = date
        self.customer = customer

    def __str__(self):
        return f"TicketPurchase(id={self.id}, time={self.time}, date={self.date}, customer={self.customer})"
    
    def insert(self, cursor: sqlite3.Cursor):
        query = "INSERT INTO TicketPurchase (id, time, date, customer) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.id, self.time, self.date, self.customer.id))
    
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE TicketPurchase SET time = ?, date = ?, customer = ? WHERE id = ?"
        cursor.execute(query, (self.time, self.date, self.customer.id, self.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM TicketPurchase WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting TicketPurchase: {e}")
            return False
        
    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['TicketPurchase']:
        query = "SELECT * FROM TicketPurchase WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return TicketPurchase(row[0], row[1], row[2], CustomerProfile.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_by_time_date_and_customer(cursor: sqlite3.Cursor, time: str, date: datetime.date, customer: CustomerProfile) -> Optional['TicketPurchase']:
        query = "SELECT * FROM TicketPurchase WHERE time = ? AND date = ? AND customer = ?"
        cursor.execute(query, (time, date, customer.id))
        row = cursor.fetchone()
        if row:
            return TicketPurchase(row[0], row[1], row[2], CustomerProfile.get_by_id(cursor, row[3]))
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['TicketPurchase']:
        query = "SELECT * FROM TicketPurchase"
        cursor.execute(query)
        rows = cursor.fetchall()
        ticket_purchase = []
        for row in rows:
            ticket_purchase.append(TicketPurchase(row[0], row[1], row[2], CustomerProfile.get_by_id(cursor, row[3])))
        return ticket_purchase
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, ticketpurchase_list: List['TicketPurchase']) -> None:
        query = """
        INSERT INTO TicketPurchase (time, date, customer) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(time, date, customer) DO NOTHING
        """
        values = [(ticket_purchase.time, ticket_purchase.date, ticket_purchase.customer.id) for ticket_purchase in ticketpurchase_list]
        cursor.executemany(query, values)

class Ticket():
    def __init__(self, id: int, screening: Screening, chair: Chair, ticketpirce: TicketPrice, ticketPurchase: TicketPurchase):
        self.id = id
        self.screening = screening
        self.chair = chair
        self.ticketpirce = ticketpirce
        self.ticketPurchase = ticketPurchase

    def __str__(self):
        return f"Ticket(id={self.id}, screening={self.screening}, chair={self.chair}, ticketpirce={self.ticketpirce}, ticketPurchase={self.ticketPurchase})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Ticket (id, screening, chair, price, purchase) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.screening.id, self.chair.id, self.ticketpirce.id, self.ticketPurchase.id))

    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Ticket WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Ticket: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Ticket SET screening = ?, chair = ?, ticketpirce = ?, ticketPurchase = ? WHERE id = ?"
        cursor.execute(query, (self.screening.id, self.chair.id, self.ticketpirce.id, self.ticketPurchase.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Ticket']:
        query = "SELECT * FROM Ticket WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Ticket(row[0], Screening.get_by_id(cursor, row[1]), Chair.get_by_id(cursor, row[2]), TicketPrice.get_by_id(cursor, row[3]), TicketPurchase.get_by_id(cursor, row[4]))
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Ticket']:
        query = "SELECT * FROM Ticket"
        cursor.execute(query)
        rows = cursor.fetchall()
        tickets = []
        for row in rows:
            tickets.append(Ticket(row[0], Screening.get_by_id(cursor, row[1]), Chair.get_by_id(cursor, row[2]), TicketPrice.get_by_id(cursor, row[3]), TicketPurchase.get_by_id(cursor, row[4])))
        return tickets
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, purchase_list: List['Ticket']) -> None:
        query = """
        INSERT INTO Ticket (screening, chair, price, purchase) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(screening, chair, price, purchase) DO NOTHING
        """
        values = [(ticket.screening.id, ticket.chair.id, ticket.ticketpirce.id, ticket.ticketPurchase.id) for ticket in purchase_list]
        cursor.executemany(query, values)    

    @staticmethod
    def get_amount_by_play_and_date(cursor: sqlite3.Cursor, id: int, date: str):
        query = """
        SELECT COUNT(*) FROM Ticket 
        JOIN Screening ON Ticket.screening = Screening.id 
        WHERE Screening.play = ? AND Screening.date = ?
        """  
        cursor.execute(query, (id, date,))
        count = cursor.fetchone()
        return count if count else None

class Act():
    def __init__(self, id: int, number: int, play: Play, name: str = None):
        self.id = id
        self.number = number
        self.name = name
        self.play = play

    def __str__(self):
        return f"Act(id={self.id}, number={self.number}, name={self.name})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Act (id, number, name, play) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.number, self.name, self.play.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Act WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Act: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Act SET number = ?, name = ?, play = ? WHERE id = ?"
        cursor.execute(query, (self.number, self.name, self.play.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Act']:
        query = "SELECT * FROM Act WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Act(row[0], row[1], row[2], Play.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_by_number_and_play(cursor: sqlite3.Cursor, number: int, play: Play) -> Optional['Act']:
        query = "SELECT * FROM Act WHERE number = ? AND play = ?"
        cursor.execute(query, (number, play.id))
        row = cursor.fetchone()
        if row:
            return Act(row[0], row[1], row[2], play)
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Act']:
        query = "SELECT * FROM Act"
        cursor.execute(query)
        rows = cursor.fetchall()
        acts = []
        for row in rows:
            acts.append(Act(row[0], row[1], row[2], Play.get_by_id(cursor, row[3])))
        return acts
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, act_list: List['Act']) -> None:
        query = """
        INSERT INTO Act (number, name, play) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(number, play) DO NOTHING
        """
        values = [(act.number, act.name, act.play.id) for act in act_list]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_acts_by_actor(cursor: sqlite3.Cursor, name: str):
        query = """
        SELECT * FROM Act WHERE id = (
          SELECT (act) FROM RoleActJunction WHERE role = (
            SELECT (role) FROM ActorRoleJunction WHERE actor = (
              SELECT (id) FROM Actor WHERE name = ?
            )
          )
        )
        """
        cursor.execute(query, (name,))
        rows = cursor.fetchall()
        acts = []
        if rows:
            for row in rows:
                acts.append(Act(row[0], row[1], row[3], row[2]))
            return acts
        return None

class Actor():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    
    def __str__(self):
        return f"Actor(id={self.id}, name={self.name})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Actor (id, name) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Actor WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Actor: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Actor SET name = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Actor']:
        query = "SELECT * FROM Actor WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Actor(row[0], row[1])
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str) -> Optional['Actor']:
        query = "SELECT * FROM Actor WHERE name = ?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            return Actor(row[0], row[1])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Actor']:
        query = "SELECT * FROM Actor"
        cursor.execute(query)
        rows = cursor.fetchall()
        actors = []
        for row in rows:
            actors.append(Actor(row[0], row[1]))
        return actors
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, actor_list: List['Actor']) -> None:
        query = """
        INSERT INTO Actor (name) VALUES (?)
        ON CONFLICT(id) DO NOTHING
        """
        values = [(actor.name,) for actor in actor_list]
        cursor.executemany(query, values)
    
    @staticmethod
    def get_all_by_play(cursor: sqlite3.Cursor, play_id: int):
        query = """
        SELECT * FROM Actor WHERE id = (
          SELECT (id) FROM ActorRoleJunction WHERE role = (
            SELECT (id) FROM RoleActJunction WHERE act = (
              SELECT (id) FROM Act WHERE play = ?
            )
          )
        )
        """
        cursor.execute(query, (play_id,))
        rows = cursor.fetchall()
        actors = []
        if rows:
            for row in rows:
                actors.append(Actor(row[0], row[1]))
            return actors
        return None
    
    @staticmethod
    def get_actors_by_act(cursor: sqlite3.Cursor, actId: int):
        query = """
        SELECT Actor.name, Play.name FROM Actor 
        LEFT OUTER JOIN ActorRoleJunction 
          ON Actor.id = ActorRoleJunction.actor
        LEFT OUTER JOIN RoleActJunction
          ON ActorRoleJunction.role = RoleActJunction.role
        LEFT OUTER JOIN Act
          ON RoleActJunction.act = Act.id
        LEFT OUTER JOIN Play
          ON Act.play = Play.id
        WHERE RoleActJunction.act = ?
        """
        cursor.execute(query, (actId,))
        rows = cursor.fetchall()
        actors = []
        if rows:
            for row in rows:
                actors.append((f'Actor={row[0]} Play={row[1]}'))
            return actors
        return None
    
class Role():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Role(id={self.id}, name={self.name})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Role (id, name) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Role WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Role: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Role SET name = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Role']:
        query = "SELECT * FROM Role WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Role(row[0], row[1])
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str) -> Optional['Role']:
        query = "SELECT * FROM Role WHERE name = ?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            return Role(row[0], row[1])
        return None

    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Role']:
        query = "SELECT * FROM Role"
        cursor.execute(query)
        rows = cursor.fetchall()
        roles = []
        for row in rows:
            roles.append(Role(row[0], row[1]))
        return roles
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, role_list: List['Role']) -> None:
        query = """
        INSERT INTO Role (name) VALUES (?)
        ON CONFLICT(id) DO NOTHING
        """
        values = [(roles.name,) for roles in role_list]
        cursor.executemany(query, values)
    

class RoleActJunction():
    def __init__(self, act: Act, role: Role):
        self.act = act
        self.role = role

    def __str__(self):
        return f"RoleActJunction(act={self.act}, role={self.role})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO RoleActJunction (act, role) VALUES (?, ?)
        ON CONFLICT(act, role) DO NOTHING  
        """
        cursor.execute(query, (self.act.id, self.role.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM RoleActJunction WHERE act = ? AND role = ?"
            cursor.execute(query, (self.act.id, self.role.id))
            return True
        except Exception as e:
            print(f"Error deleting RoleActJunction: {e}")
            return False
        
    @staticmethod
    def get_by_act(cursor: sqlite3.Cursor, act: Act) -> List['RoleActJunction']:
        query = "SELECT * FROM RoleActJunction WHERE act = ?"
        cursor.execute(query, (act.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RoleActJunction(act, Role.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_role(cursor: sqlite3.Cursor, role: Role) -> List['RoleActJunction']:
        query = "SELECT * FROM RoleActJunction WHERE role = ?"
        cursor.execute(query, (role.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RoleActJunction(Act.get_by_id(cursor, row[0]), role))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['RoleActJunction']:
        query = "SELECT * FROM RoleActJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(RoleActJunction(Act.get_by_id(cursor, row[0]), Role.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['RoleActJunction']) -> None:
        query = """
        INSERT INTO RoleActJunction (act, role) VALUES (?, ?)
        ON CONFLICT(act, role) DO NOTHING
        """
        values = [(junction.act.id, junction.role.id) for junction in junction_list]
        cursor.executemany(query, values)
        
    

class ActorRoleJunction():
    def __init__(self, actor: Actor, role: Role):
        self.actor = actor
        self.role = role

    def __str__(self):
        return f"ActorRoleJunction(actor={self.actor}, role={self.role})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO ActorRoleJunction (actor, role) VALUES (?, ?)
        ON CONFLICT(actor, role) DO NOTHING
        """
        cursor.execute(query, (self.actor.id, self.role.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM ActorRoleJunction WHERE actor = ? AND role = ?"
            cursor.execute(query, (self.actor.id, self.role.id))
            return True
        except Exception as e:
            print(f"Error deleting ActorRoleJunction: {e}")
            return False
        
    @staticmethod
    def get_by_actor(cursor: sqlite3.Cursor, actor: Actor) -> List['ActorRoleJunction']:
        query = "SELECT * FROM ActorRoleJunction WHERE actor = ?"
        cursor.execute(query, (actor.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(ActorRoleJunction(actor, Role.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_role(cursor: sqlite3.Cursor, role: Role) -> List['ActorRoleJunction']:
        query = "SELECT * FROM ActorRoleJunction WHERE role = ?"
        cursor.execute(query, (role.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(ActorRoleJunction(Actor.get_by_id(cursor, row[0]), role))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['ActorRoleJunction']:
        query = "SELECT * FROM ActorRoleJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(ActorRoleJunction(Actor.get_by_id(cursor, row[0]), Role.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['ActorRoleJunction']) -> None:
        query = """
        INSERT INTO ActorRoleJunction (actor, role) VALUES (?, ?)
        ON CONFLICT(actor, role) DO NOTHING
        """
        values = [(junction.actor.id, junction.role.id) for junction in junction_list]
        cursor.executemany(query, values)

class Task():
    def __init__(self, id: int, name: str, play: Play):
        self.id = id
        self.name = name
        self.play = play

    def __str__(self):
        return f"Task(id={self.id}, name={self.name}, play={self.play})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Task (id, name, play) VALUES (?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name, self.play.id))

    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Task WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Task: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Task SET name = ?, play = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.play.id, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Task']:
        query = "SELECT * FROM Task WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            return Task(row[0], row[1], row[2], Play.get_by_id(cursor, row[3]))
        return None
    
    @staticmethod
    def get_by_name_and_play(cursor: sqlite3.Cursor, name: str, play: Play) -> Optional['Task']:
        query = "SELECT * FROM Task WHERE name = ? AND play = ?"
        cursor.execute(query, (name, play.id))
        row = cursor.fetchone()
        if row:
            return Task(row[0], row[1], play)
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Task']:
        query = "SELECT * FROM Task"
        cursor.execute(query)
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Task(row[0], row[1], row[2], Play.get_by_id(cursor, row[3])))
        return tasks
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, task_list: List['Task']) -> None:
        query = """
        INSERT INTO Task (name, play) VALUES (?, ?)
        ON CONFLICT(id) DO NOTHING
        ON CONFLICT(name, play) DO NOTHING
        """
        values = [(task.name, task.play.id) for task in task_list]
        cursor.executemany(query, values)


class EmployeeStatus():
    def __init__(self, status: str):
        self.status = status

    def __str__(self):
        return f"EmployeeStatus(status={self.status})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO EmployeeStatus (employee_status) VALUES (?)
        ON CONFLICT(status) DO NOTHING
        """
        cursor.execute(query, (self.status,))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM EmployeeStatus WHERE employee_status = ?"
            cursor.execute(query, (self.status,))
            return True
        except Exception as e:
            print(f"Error deleting EmployeeStatus: {e}")
            return False

    @staticmethod
    def get_by_status(cursor: sqlite3.Cursor, status: str) -> Optional['EmployeeStatus']:
        query = "SELECT * FROM EmployeeStatus WHERE employee_status = ?"
        cursor.execute(query, (status,))
        row = cursor.fetchone()
        if row:
            return EmployeeStatus(row[0])
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['EmployeeStatus']:
        query = "SELECT * FROM EmployeeStatus"
        cursor.execute(query)
        rows = cursor.fetchall()
        statusene = []
        for row in rows:
            statusene.append(EmployeeStatus(row[0]))
        return statusene
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, status_list: List['EmployeeStatus']) -> None:
        query = """
        INSERT INTO EmployeeStatus (employee_status) VALUES (?)
        ON CONFLICT(employee_status) DO NOTHING
        """
        values = [(status.status,) for status in status_list]
        cursor.executemany(query, values)

class Contributor():
    def __init__(self, id: int, name: str, email: str, status: EmployeeStatus):
        self.id = id
        self.name = name
        self.email = email
        self.status = status

    def __str__(self):
        return f"Contributor(id={self.id}, name={self.name}, email={self.email}, status={self.status})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO Contributor (id, name, email, employee_status) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        cursor.execute(query, (self.id, self.name, self.email, self.status.status))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM Contributor WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True
        except Exception as e:
            print(f"Error deleting Contributor: {e}")
            return False
        
    def update(self, cursor: sqlite3.Cursor) -> None:
        query = "UPDATE Contributor SET name = ?, email = ?, employee_status = ? WHERE id = ?"
        cursor.execute(query, (self.name, self.email, self.status.status, self.id))

    @staticmethod
    def get_by_id(cursor: sqlite3.Cursor, id: int) -> Optional['Contributor']:
        query = "SELECT * FROM Contributor WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            status = EmployeeStatus(row[3])
            return Contributor(row[0], row[1], row[2], status)
        return None
    
    @staticmethod
    def get_by_name(cursor: sqlite3.Cursor, name: str) -> Optional['Contributor']:
        query = "SELECT * FROM Contributor WHERE name = ?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            status = EmployeeStatus(row[3])
            return Contributor(row[0], row[1], row[2], status)
        return None
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['Contributor']:
        query = "SELECT * FROM Contributor"
        cursor.execute(query)
        rows = cursor.fetchall()
        contributor = []
        for row in rows:
            status = EmployeeStatus(row[3])
            contributor.append(Contributor(row[0], row[1], row[2], status))
        return contributor
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, contributor_list: List['Contributor']) -> None:
        query = """
        INSERT INTO Contributor (name, email, employee_status) VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO NOTHING
        """
        values = [(contributor.name, contributor.email, contributor.status.status) for contributor in contributor_list]
        cursor.executemany(query, values)


class TaskContributorJunction():
    contributor: Contributor
    task: Task

    def __init__(self, contributor: Contributor, task: Task):
        self.contributor = contributor
        self.task = task

    def __str__(self):
        return f"TaskContributorJunction(contributor={self.contributor}, task={self.task})"
    
    def insert(self, cursor: sqlite3.Cursor) -> None:
        query = """
        INSERT INTO TaskContributorJunction (contributor, task) VALUES (?, ?)
        ON CONFLICT(contributor, task) DO NOTHING
        """
        cursor.execute(query, (self.contributor.id, self.task.id))
    
    def delete(self, cursor: sqlite3.Cursor) -> bool:
        try:
            query = "DELETE FROM TaskContributorJunction WHERE contributor = ? AND task = ?"
            cursor.execute(query, (self.contributor.id, self.task.id))
            return True
        except Exception as e:
            print(f"Error deleting TaskContributorJunction: {e}")
            return False
        
    @staticmethod
    def get_by_contributor(cursor: sqlite3.Cursor, contributor: Contributor) -> List['TaskContributorJunction']:
        query = "SELECT * FROM TaskContributorJunction WHERE contributor = ?"
        cursor.execute(query, (contributor.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(TaskContributorJunction(contributor, Task.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def get_by_task(cursor: sqlite3.Cursor, task: Task) -> List['TaskContributorJunction']:
        query = "SELECT * FROM TaskContributorJunction WHERE task = ?"
        cursor.execute(query, (task.id,))
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(TaskContributorJunction(Contributor.get_by_id(cursor, row[0]), task))
        return junctions
    
    @staticmethod
    def get_all(cursor: sqlite3.Cursor) -> List['TaskContributorJunction']:
        query = "SELECT * FROM TaskContributorJunction"
        cursor.execute(query)
        rows = cursor.fetchall()
        junctions = []
        for row in rows:
            junctions.append(TaskContributorJunction(Contributor.get_by_id(cursor, row[0]), Task.get_by_id(cursor, row[1])))
        return junctions
    
    @staticmethod
    def upsert_batch(cursor: sqlite3.Cursor, junction_list: List['TaskContributorJunction']) -> None:
        query = """
        INSERT INTO TaskContributorJunction (contributor, task) VALUES (?, ?)
        ON CONFLICT(contributor, task) DO NOTHING
        """
        values = [(junction.contributor.id, junction.task.id) for junction in junction_list]
        cursor.executemany(query, values)
