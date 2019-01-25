import sqlite3

conn = sqlite3.connect('hotel.db')

conn.execute("""CREATE TABLE Customers(
	cID VARCHAR(30) NOT NULL,
	name VARCHAR(30) NOT NULL,
	email VARCHAR(30) NOT NULL,
	phNo int,
	PRIMARY KEY(cID)
);""")

conn.execute("""CREATE TABLE Rooms(
	roomNo int NOT NULL,
	maxHeads int,
	category int,
	PRIMARY KEY(roomNo),
    FOREIGN KEY(category) REFERENCES Price(category)
);""")

conn.execute("""CREATE TABLE Price(
	category int,
	basePrice int,
	pricePerHead int,
	pricePerDay int,
    PRIMARY KEY(category)
);""")

conn.execute("""CREATE TABLE Bills(
	invoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
	amount int,
	generationDate date
);""")

conn.execute("""CREATE TABLE Booked(
    cid VARCHAR(30) NOT NULL,
    roomNo int,
    heads int,
    checkindate date,
    checkoutdate date,
	invoiceid int
	);""")

conn.commit()
 
conn.close()