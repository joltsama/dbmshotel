#!/usr/bin/python3
import os

from flask import Flask, url_for, redirect, flash, request, json
from flask import render_template, make_response, session
from .forms import BookForm, CheckStatus, CancelBooking, SelectRoom
from .sql import *

def create_app(test_config=None):
    # create and configure the app
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

    # ensure the instance folder exists
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
            request.form['room']
            )
            
            if code['roomno']==None:
                flash(f"No room available", "fail")
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
            bookRoom(request.form['identity'], 
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
            flash(f"Room booked successfully!", "success")
            return redirect(url_for('checkstatus'))
        return render_template('book.html', roomdata=json.loads(roomdata), form=form)

    @app.route('/checkstatus', methods=['GET','POST'])
    def checkstatus():
        form = CheckStatus()
        if form.validate_on_submit():
            bookingid=request.form['bookingid']
            checkin=request.form['checkin']
            session['status']=json.dumps({'bookingid':bookingid, 'checkin':checkin}) #just for bill
            return redirect(url_for('status', bookingid=bookingid, checkin=checkin))
        return render_template('checkstatus.html', form = form)

    @app.route('/status/<bookingid>/<checkin>')
    def status(bookingid, checkin):
        if request.method=='GET':
            rows=checkStatus(bookingid, checkin)
            return render_template ('status.html', rows=rows)
        else:
            return redirect (url_for('home'))

    @app.route('/bill')
    def bill():
        if request.method=='GET':
            billrequired=json.loads(session.pop('status',None))
            rows=generateBill(billrequired['bookingid'], billrequired['checkin'])
            return render_template ('bill.html', rows=rows)
        else:
            return redirect (url_for('home'))

    @app.route('/cancelbooking', methods=['GET','POST'])
    def cancel_booking():
        form = CancelBooking()
        if form.validate_on_submit():
            flash(f"Booking canceled!", "success")
            return redirect(url_for('home'))
        return render_template('cancelbooking.html', form = form)

    @app.route('/user/<username>')
    def profile(username):
        return render_template('user.html', username=username)

    return app


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
