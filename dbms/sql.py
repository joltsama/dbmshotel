#!/usr/bin/python3
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
        sql="select checkindate,checkoutdate from booked where roomno="+str(rn[0])
        cursor.execute(sql)
        ddd=cursor.fetchall()
        if(len(ddd)==0):
            r=rn[0]
            break
    if(r==-1):
        for i in range(0,len(ddd)):
            if( outDate<str(ddd[i][0]) ):
                if( inDate>str(ddd[i-1][1]) ):
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
    return(final)


def bookRoom(cID,name,phNo,email,heads,inDate,outDate,category,roomNo,amount):
      
    sql="SELECT datetime('now')"
    cursor.execute(sql)
    x=cursor.fetchone()
    datenow=x[0]

    rr=getRoom(heads, inDate, outDate, category)
    
    if rr==None:
        return False

    sql="select count(*) from customers where cId='"+str(cID)+"'"
    cursor.execute(sql)
    x=cursor.fetchone()

    if(x[0]==0):
        sql="INSERT INTO customers(cid,name,email,phno) VALUES(?,?,?,?)"
        cursor.execute(sql,(cID,name,email,phNo,))

    sql="INSERT INTO Bills(amount,generationdate) VALUES(?,?)"
    cursor.execute(sql,(amount,datenow))

    sql="SELECT count(*) from Bills"
    cursor.execute(sql)
    x=cursor.fetchone()
    inv=x[0]

    sql="INSERT INTO Booked(cid,roomNo,heads,checkindate,checkoutdate,invoiceid) VALUES(?,?,?,?,?,?)"
    cursor.execute(sql,(cID,roomNo,heads,inDate,outDate,inv))


    conn.commit()
    #conn.close()


def checkStatus(cID,inDate):
    final=False
    sql="select count(*) from booked where cid='"+str(cID)+"'"+"and checkindate='"+str(inDate)+"'"
    cursor.execute(sql)
    y=cursor.fetchone()
    if(y[0]!=0):
        sql="select * from booked where cid='"+str(cID)+"'"+"and checkindate='"+str(inDate)+"'"
        cursor.execute(sql)
        y=cursor.fetchall()
        y=y[0]
        sql="select * from customers where cid='"+str(cID)+"'"
        cursor.execute(sql)
        x=cursor.fetchone()

        final={
            "name" : x[1],
            "email" : x[2],
            "phoneno" : x[3],
            "checkin" : y[3],
            "checkout" : y[4],
            "roomno" : y[1]
        }
    return(final)


def generateBill(cID,inDate):

    sql="select count(*) from booked where cid='"+str(cID)+"'"+"AND checkindate='"+str(inDate)+"'"
    cursor.execute(sql)
    x=cursor.fetchone()
    final=False
    if(x[0]!=0):
        sql="select * from booked where cid='"+str(cID)+"'"+"AND checkindate='"+str(inDate)+"'"
        cursor.execute(sql)
        x=cursor.fetchall()
        x=x[0]
        inv=x[5]

        #sql="select * from bills where invoiceid='"+str(inv)+"'"
        sql="select * from bills where invoiceid='{}'".format(str(inv))
        cursor.execute(sql)
        y=cursor.fetchone()

        sql="select * from customers where cid='"+str(cID)+"'"
        cursor.execute(sql)
        z=cursor.fetchone()
        final={
            "name" : z[1],
            "phoneno" : z[3],
            "email" : z[2],
            "checkin" : x[3],
            "checkout" : x[4],
            "amount" : y[1],
            "invoiceid" : y[0]
        }
        #conn.close()
    return(final)


def cancelBooking(inID):

    sql="SELECT count(*) FROM Bills WHERE invoiceID='"+str(inID)+"'"
    cursor.execute(sql)
    x=cursor.fetchone()
    if(x[0]==0):
        return(False)

    sql="DELETE FROM Booked WHERE invoiceID='"+str(inID)+"'"
    cursor.execute(sql)

    sql="DELETE FROM Bills WHERE invoiceID='"+str(inID)+"'"
    cursor.execute(sql)

    conn.commit()

    return True