#!/usr/bin/python3
import os

from flask import Flask, url_for, redirect, flash, request
from flask import render_template
from .forms import BookForm, CheckStatus, CancelBooking
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


    checkdb()

    
    # PAGES
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/checkstatus', methods=['GET','POST'])
    def checkstatus():
        form = CheckStatus()
        if form.validate_on_submit():
            bookingid=request.form['bookingid']
            return redirect(url_for('status', bookingid=bookingid))
        return render_template('checkstatus.html', form = form)

    @app.route('/status/<bookingid>')
    def status(bookingid):
        if request.method=='GET':
            rows=bill(bookingid)
            # rows={'bookingid':'sdf', 
            # 'name': 'Pedo', 
            # 'email': 'sdf',
            # 'checkin': '322',
            # 'checkout': '11', 
            # 'room': '123'}
            return render_template ('status.html', rows=rows)
        else:
            return redirect (url_for('home'))

    @app.route('/book', methods=['GET','POST'])
    def book():
        form = BookForm()
        if form.validate_on_submit():
            code=bookRoom(request.form['identity'], 
            request.form['username'], 
            request.form['email'],
            request.form['phoneno'], 
            request.form['checkin'], 
            request.form['checkout'],
            request.form['room'])
            if code==-1:
                flash(f"No room available", "fail")
            else:
                flash(f"Room booked successfully!", "fail")
            return redirect(url_for('home'))
        return render_template('book.html', form=form)

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
