#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms_components import DateRange
from datetime import datetime, date

class BookForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phoneno = IntegerField('Phone number', validators=[NumberRange(min=1, max=10)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=30)])
    identity = StringField('Identity Card', validators=[DataRequired(), Length(min=20, max=20)])
    checkin = DateField('Checkin Date', validators=[DateRange(min=date.today())])
    checkout = DateField('Checkout Date', validators=[DateRange(min=date.today())])
    room = RadioField('Room Type', validators=[DataRequired()], choices=[('1','Room1'), ('2','Room2'), ('3','Room3')])
    submit = SubmitField('Submit')


class CheckStatus(FlaskForm):
    bookingid = StringField('Booking ID', validators=[DataRequired(), Length(min=20, max=20)])
    submit = SubmitField('Check')

class CancelBooking(FlaskForm):
    bookingid = StringField('Booking ID', validators=[DataRequired(), Length(min=20, max=20)])
    submit = SubmitField('Cancel')


