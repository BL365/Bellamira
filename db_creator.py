import sqlite3
from sqlite3 import OperationalError


class dbCreator:

    dbName = "BellamiraHallDB"

    createTablePeopleSQL = """CREATE TABLE IF NOT EXISTS people (
        id INT AUTO_INCREMENT,
        FIO TEXT,
        login TEXT,
        password TEXT,
        phone TEXT,
        link TEXT,
        primary key (id)
    )"""

    createTableHallSQL = """CREATE TABLE IF NOT EXISTS hall (
        id INT AUTO_INCREMENT,
        name TEXT,
        square REAL,
        primary key (id)
    )"""

    createTableRenterSQL = """CREATE TABLE IF NOT EXISTS renters (
        id INT AUTO_INCREMENT,
        name TEXT,
        phone TEXT,
        link TEXT,
        people_id INT,
        primary key (id)
    )"""

    createTableRenterGroupSQL = """CREATE TABLE IF NOT EXISTS renters_group (
        id INT AUTO_INCREMENT,
        renter_id INT,
        name TEXT,
        people_id INT,
        primary key (id)
    )"""

    createTableGroupPeopleSQL = """CREATE TABLE IF NOT EXISTS group_people (
        renter_id INT,
        group_id INT,
        people_id INT,
        primary key (renter_id, group_id, people_id)
    )"""

    createTableHallUsingSQL = """CREATE TABLE IF NOT EXISTS using_hall (
        id INT AUTO_INCREMENT,
        name TEXT,
        group_id INT,
        hall_id INT,
        start_time INT,
        end_time INT,
        primary key (id, group_id, hall_id, start_time)
    )"""

    createTableHallPriceSQL = """CREATE TABLE IF NOT EXISTS hall_price (
        id INT AUTO_INCREMENT,
        hall_id INT,
        renter_id,
        start_date INT,
        end_date INT,
        time_zone_id INT,
        price REAL,
        primary key (id)
    )"""

    createTableTimeZoneSQL = """CREATE TABLE IF NOT EXISTS time_zone (
        id INT AUTO_INCREMENT,
        hall_id INT,
        days_of_week TEXT,
        start_time INT,
        end_time INT,
        cost REAL,
        primary key (id)
    )"""

    createTableRateRenter = """CREATE TABLE IF NOT EXISTS rate_renter (
        id INT AUTO_INCREMENT,
        hall_id INT,
        days_of_week TEXT,
        renter_id INT,
        start_time INT,
        end_time INT,
        cost REAL,
        primary key (id)
    )"""

    createTablePaysSQL = """CREATE TABLE IF NOT EXISTS pays (
        id INT AUTO_INCREMENT,
        date INT,
        renter_id INT,

        sum REAL,
        primary key (id)
    )"""

    createTableChargesSQL = """CREATE TABLE IF NOT EXISTS charges (
        id INT AUTO_INCREMENT,
        date INT,
        position_id INT,
        description TEXT,
        sum REAL,
        primary key (id)
    )"""

    createTablePositionsSQL = """CREATE TABLE IF NOT EXISTS positions (
        id INT AUTO_INCREMENT,
        description TEXT,
        primary key (id)
    )"""




    def execute(self):
        conn = sqlite3.connect(self.dbName)
        try:
            conn.execute(self.createTablePeopleSQL)
            conn.execute(self.createTableRenterSQL)
            conn.execute(self.createTableHallSQL)
            conn.execute(self.createTablePositionsSQL)
            conn.execute(self.createTableRenterGroupSQL)
            conn.execute(self.createTableGroupPeopleSQL)
            conn.execute(self.createTableTimeZoneSQL)
            conn.execute(self.createTableChargesSQL)
            conn.execute(self.createTableHallPriceSQL)
            conn.execute(self.createTableHallUsingSQL)
            conn.execute(self.createTablePaysSQL)
            conn.execute(self.createTableRateRenter)

        except OperationalError, msg:
            print msg
        conn.close()