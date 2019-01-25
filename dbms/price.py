import sqlite3
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

sql="INSERT INTO PRICE (category,basePrice,pricePerHead,pricePerDay) VALUES(?,?,?,?)"\

def insP(category,basePrice,pricePerHead,pricePerDay):
    cursor.execute(sql,(category,basePrice,pricePerHead,pricePerDay))

insP(1,1000,300,500)
insP(2,700,200,400)
insP(3,500,200,300)

conn.commit()