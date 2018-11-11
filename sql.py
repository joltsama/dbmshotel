import sqlite3, os
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()
     
def createtable():
		
	conn = sqlite3.connect('hotel.db')

	conn.executescript("""CREATE TABLE Customers(
		cID VARCHAR(30) NOT NULL,
		name VARCHAR(30) NOT NULL,
		email VARCHAR(30) NOT NULL,
		phNo int,
		inDate DATE NOT NULL,
		outDate DATE NOT NULL,
		CHECK(inDate<outDate),
		PRIMARY KEY(cID)
	);CREATE TABLE Rooms(
		roomNo int NOT NULL,
		cID int DEFAULT NULL,
		category int,
		availability VARCHAR(3) DEFAULT 'yes',
		PRIMARY KEY(roomNo),
		FOREIGN KEY(cID) REFERENCES Customers(cID),
		FOREIGN KEY(category) REFERENCES Roomcategory(category)
	);""")

	conn.close()

def checkdb():
    if not os.path.isfile("hotel.db"):
        createtable()

def bill(cID):
    sql="select roomno, julianday(outdate)-julianday(indate) as dd from customers where cid='"+cID+"';"
    cursor.execute(sql)
    x=cursor.fetchall()
    for y in x:
        print (y)
    rn=x[0][0]
    days=x[0][1]
    sql="select category from rooms where roomno="+str(rn)
    cursor.execute(sql)
    x=cursor.fetchall()
    ct=x[0]
    rent=1000
    if(ct==1):
        rent=2500
    elif(ct==2):
        rent=1500
    elif(ct==3):
        rent=1000

    sql="select * from customers where cid='"+cID+"';"
    cursor.execute(sql)
    x=cursor.fetchone()

    final={
        "identity" :  x[0],
        "name" : x[1],
        "email" : x[2],
        "phoneno" : x[3],
        "checkin" : x[4],
        "checkout" : x[5],
        "room" : x[6],
        "total" : days*rent
    }

    return(final)

def bookRoom(cID,name,email,phNo,inDate,outDate,category):
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    sql = "select roomNo from Rooms where category="+str(category)
    cursor.execute(sql)
    roomNo=cursor.fetchall()
    r=-1
    for rn in roomNo:
        sql="select cid from customers where roomno="+str(rn[0])
        cursor.execute(sql)
        ci=cursor.fetchall()
        if(len(ci)==0):
            r=rn[0]
            break
    if(r==-1):
        for rn in roomNo:
            sql="select indate,outdate from customers where roomno="+str(rn[0])+"order by indate"
            cursor.execute(sql)
            ci=cursor.fetchall()
            for i in range(0,len(ci)):
                if( outDate<str(ci[i][0]) ):
                    if( inDate>str(ci[i-1][1]) ):
                        r=rn[0]
                        break

    if(r==-1):
        return(r) #fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    else:
        sql="INSERT INTO customers(cid,name,email,phno,indate,outdate,roomno) VALUES(?,?,?,?,?,?,?)"
        cursor.execute(sql,(cID,name,phNo,inDate,outDate,r))
        conn.commit()
        return r
