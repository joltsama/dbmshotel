#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo
from wtforms_components import DateRange
from datetime import datetime, date

class BookForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phoneno = IntegerField('Phone number', validators=[NumberRange(min=6000000000, max=9999999999)])
    #address = StringField('Address', validators=[DataRequired(), Length(min=5, max=30)])
    identity = StringField('Identity Card', validators=[DataRequired(), Length(min=10, max=20)])
    #checkin = DateField('Checkin Date', validators=[DateRange(min=date.today())])
    #checkout = DateField('Checkout Date', validators=[DateRange(min=date.today())])
    #room = RadioField('Room Type', validators=[DataRequired()], choices=[('1','Room1'), ('2','Room2'), ('3','Room3')])
    submit = SubmitField('Pay')


class SelectRoom(FlaskForm):
    heads = IntegerField('No of adults', validators=[NumberRange(min=1, max=3)])
    checkin = DateField('Checkin Date', validators=[DateRange(min=date.today())])
    checkout = DateField('Checkout Date', validators=[DateRange(min=date.today())])
    room = RadioField('Room Type', validators=[DataRequired()], choices=[('1','Room Type 1'), ('2','Room Type 2'), ('3','Room Type 3')])
    submit = SubmitField('Select')

class CheckStatus(FlaskForm):
    bookingid = StringField('Booking ID', validators=[DataRequired(), Length(min=1, max=20)])
    checkin = DateField('Checkin Date', validators=[DateRange(min=date.today())])
    submit = SubmitField('Check')

class AdminLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Check')


class AdminCP(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class CancelBooking(FlaskForm):
    invoiceid = StringField('Invoice ID', validators=[DataRequired(), Length(min=1, max=20)])
    #checkin = DateField('Checkin Date', validators=[DateRange(min=date.today())])
    submit = SubmitField('Submit')


