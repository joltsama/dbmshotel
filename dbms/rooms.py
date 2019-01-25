import sqlite3
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

sql = "INSERT INTO Rooms(roomNo,category,maxHeads) VALUES(?,?,?)"

def insR(roomNo,category,maxHeads):
    cursor.execute(sql,(roomNo,category,maxHeads))

for i in range(101,116):
    insR(i,3,3)

for i in range(201,216):
    insR(i,3,3)

for i in range(301,316):
    insR(i,2,3)

for i in range(401,416):
    insR(i,2,3)

for i in range(501,516):
    insR(i,1,3)

conn.commit()