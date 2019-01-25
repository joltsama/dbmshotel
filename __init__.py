#!/usr/bin/python3
import os

from flask import Flask, url_for, redirect, flash, request, json
from flask import render_template, make_response, session
from .forms import BookForm, CheckStatus, CancelBooking, SelectRoom, AdminLogin, AdminCP
from .sql import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///hotel.db',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        TEMPLATES_AUTO_RELOAD=True,
    )
    app.debug=True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    
    # PAGES
    @app.route('/')
    def home():
        return render_template('home.html')


    @app.route('/selectroom', methods=['GET','POST'])
    def selectroom():
        form = SelectRoom()
        if form.validate_on_submit():
            roomdata={'heads': request.form['heads'],
            'checkin': request.form['checkin'],
            'checkout': request.form['checkout'],
            'room': request.form['room']}

            code=getRoom(request.form['heads'],
            request.form['checkin'],
            request.form['checkout'],
            request.form['room'])
            
            if code['roomno']==False:
                flash(f"No rooms of this type available")
                return render_template(url_for('selectroom'))
            else:
                roomdata={**roomdata, **code}
                flash(f"Rooms available", "success")

            session['roomdata']=json.dumps(roomdata)

            return redirect(url_for('book', roomdata=roomdata))
        return render_template('selectroom.html', form=form)


    @app.route('/book', methods=['GET','POST'])
    def book():
        roomdata=session['roomdata']
        form = BookForm()

        if form.validate_on_submit():

            roomdata=json.loads(session['roomdata'])

            bookingid=request.form['identity']
            checkin=roomdata['checkin']
            
            statuscode=bookRoom(request.form['identity'], 
            request.form['username'], 
            request.form['phoneno'],
            request.form['email'],
            roomdata['heads'],
            roomdata['checkin'],
            roomdata['checkout'],
            roomdata['room'],
            roomdata['roomno'],
            roomdata['amount']

            # session.pop(['heads'], None),
            # session.pop(['checkin'], None),
            # session.pop(['checkout'], None),
            # session.pop(['room'], None),
            # session.pop(['roomno'], None),
            # session.pop(['amount'], None)
            )

            # if code==-1:
            #     flash(f"Can't book room. Please try again.", "fail")
            # else:
            # ------------------------------ CHANGED BELOW HERE
            if statuscode==False:
                flash(f"Could not book room. Please try again.")
            else:
                session['status']=json.dumps({'bookingid':bookingid, 'checkin':checkin})
                flash(f"Room booked successfully!", "success")
                return redirect(url_for('bill'))
                
             
            # ------------------------------ CHANGED TILL HERE
                #return redirect(url_for('checkstatus'))
            # ------------------------------ WAS THIS ^
            
        return render_template('book.html', roomdata=json.loads(roomdata), form=form)

    @app.route('/checkstatus', methods=['GET','POST'])
    def checkstatus():
        form = CheckStatus()
        if form.validate_on_submit():
            bookingid=request.form['bookingid']
            checkin=request.form['checkin']
            if checkStatus(bookingid,checkin)==False:
                flash(f"Please check your BookingID or Check-In Date")
            else:
                return redirect(url_for('status', bookingid=bookingid, checkin=checkin))
        return render_template('checkstatus.html', form = form)

    @app.route('/status/<bookingid>/<checkin>')
    def status(bookingid, checkin):
        if request.method=='GET':
            session['status']=json.dumps({'bookingid':bookingid, 'checkin':checkin}) #just for bill
            rows=checkStatus(bookingid, checkin)
            return render_template ('status.html', rows=rows)
        else:
            return redirect (url_for('home'))

    @app.route('/bill')
    def bill():
        if request.method=='GET':
            billrequired=json.loads(session.pop('status', None))
            rows=generateBill(billrequired['bookingid'], billrequired['checkin'])
            if rows==False:
                pass
            else:
                return render_template ('bill.html', rows=rows)
        else:
            return redirect (url_for('home'))

    @app.route('/cancelbooking', methods=['GET','POST'])
    def cancel_booking():
        form = CancelBooking()
        if form.validate_on_submit():
            invoiceid=request.form['invoiceid']
            status=cancelBooking(invoiceid)
            if status==False:
                flash(f"Could not cancel your booking.")
            else:
                return redirect(url_for('home'))
        return render_template('cancelbooking.html', form = form)


    #                          ADMIN

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        #if request.method=="POST":
            #authenticate(username, password)
            #set cookies
        #    return redirect(url_for('home'))
        return render_template('admin.html')

    @app.route('/adminlogin', methods=['GET', 'POST'])
    def adminlogin():   
        form=AdminLogin()
        if form.validate_on_submit():
            username=request.form['username']
            password=request.form['password']
            f=open("admin", "r")
            up=f.read()
            up=up.split("\n")
            f.close()

            
            #return redirect(url_for('home'))
            #authenticate(username, password)
            if username==up[0] and password==up[1]:
                #return redirect(url_for('home'))
                return redirect(url_for('admin'))
                #resp = make_response(render_template('readcookie.html'))
                #resp = make_response(redirect(url_for('admin')))
                #resp.set_cookie('userID', username)
            else:
                flash(f"Invalid username or password")
        return render_template('adminlogin.html', form=form)

    @app.route('/adminlogout')
    def adminlogout():
        #remove cookies
        return redirect(url_for('home'))

    @app.route('/admincp', methods=['GET', 'POST'])
    def admincp():
        form = AdminCP(request.form)
        if request.method == 'POST' and form.validate():
            strtowrite = form.username.data+'\n'+form.password.data+'\n'+form.email.data
            f=open("admin", "w")
            f.writelines(strtowrite)
            f.close()
            #change password
            
            return redirect(url_for('adminlogin'))
        return render_template('admincp.html', form=form)

    return app


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
