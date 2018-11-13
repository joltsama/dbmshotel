from datetime import date
import sqlite3
conn = sqlite3.connect('hotel.db', check_same_thread=False)
cursor = conn.cursor()

def getRoom(heads, inDate, outDate, category):
    inD = date(*map(int, inDate.split('-')))
    outD = date(*map(int, outDate.split('-')))
    days=(outD-inD).days

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
        r=None

    cursor.execute("""SELECT basePrice,pricePerHead,pricePerDay
        FROM Price WHERE category="""+str(category)
    )
    x=cursor.fetchone()
    bsp=x[0]
    pph=x[1]
    ppd=x[2]
    total=int(bsp)+int(pph)*int(heads)+int(ppd)*int(days)
    final={
        "roomno" : r,
        "amount" : total
    }
    #conn.close()
    return (final)


def bookRoom(cID,name,phNo,email,heads,inDate,outDate,category,roomNo,amount):
    
    sql="INSERT INTO customers(cid,name,phno,email,heads,indate,outdate,roomno) VALUES(?,?,?,?,?,?,?,?)"
    cursor.execute(sql,(cID,name,phNo,email,heads,inDate,outDate,roomNo))

    sql="SELECT datetime('now')"
    cursor.execute(sql)
    x=cursor.fetchone()
    datenow=x[0]

    sql="INSERT INTO Bills(amount,generationdate) VALUES(?,?)"
    cursor.execute(sql,(amount,datenow))

    sql="SELECT COUNT(*) FROM Bills"
    cursor.execute(sql)
    x=cursor.fetchone()
    inId=x[0]

    sql="INSERT INTO Payment (cID,invoiceID) VALUES(?,?)"
    cursor.execute(sql,(cID,inId))

    conn.commit()
    #conn.close()


def checkStatus(cID,inDate):
    sql="select * from customers where cid='"+str(cID)+"'"+"AND inDate='"+str(inDate)+"'"
    cursor.execute(sql)
    x=cursor.fetchone()

    final={
        "name" : x[1],
        "phoneno" : x[3],
        "email" : x[2],
        "checkin" : x[4],
        "checkout" : x[5],
        "room" : x[7]
    }
    #conn.close()
    return(final)


def generateBill(cID,inDate):

    sql="select * from customers where cid='"+str(cID)+"'"+"AND inDate='"+str(inDate)+"'"
    cursor.execute(sql)
    x=cursor.fetchone()

    inD = date(*map(int, inDate.split('-')))
    outD = date(*map(int, x[5].split('-')))
    days=(outD-inD).days

    sql="select category from rooms where roomno="+str(x[7])
    cursor.execute(sql)
    y=cursor.fetchone()

    category=y[0]

    cursor.execute("""SELECT basePrice,pricePerHead,pricePerDay
        FROM Price WHERE category="""+str(category)
    )
    y=cursor.fetchone()
    bsp=y[0]
    pph=y[1]
    ppd=y[2]
    total=int(bsp)+int(pph)*int(x[6])+int(ppd)*int(days)

    final={
        "name" : x[1],
        "phoneno" : x[3],
        "email" : x[2],
        "checkin" : x[4],
        "checkout" : x[5],
        "amount" : total
    }
    #conn.close()
    return(final)

def ifBooked(bookingid, checkin):
    return True

def cancelBooking(bookingid, checkin):
    return True