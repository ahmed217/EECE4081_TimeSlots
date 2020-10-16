from flask import Flask
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
from datetime import datetime
#import MySQLdb.cursors 
#import re 

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy
 
database = "sqlite:///timeslots.db"

app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. this db will be used in this project 
db = SQLAlchemy(app)
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
mysql = MySQL(app) 

@app.route('/') 
@app.route('/index')
def index():
    timeslot = timeslots.query.all()
    return render_template("index.html",timeslot=timeslot, title = 'Template')

    
@app.route('/create', methods=['GET','POST'])
def create():
    #Database string 
    #isFrist = true
    if request.form:
        if request.form.get("Sunday") == 'true':
            Sunday = True
        else:
            Sunday = False
        if request.form.get("Monday") == 'true':
            Monday = True
        else:
            Monday = False
        if request.form.get("Tuesday") == 'true':
            Tuesday = True
        else:
            Tuesday = False
        if request.form.get("Wednesday") == 'true':
            Wednesday = True
        else:
            Wednesday = False
            
        if request.form.get("Thursday") == 'true':
            Thursday = True
        else:
            Thursday = False
            
        if request.form.get("Friday") == 'true':
            Friday = True
        else:
            Friday = False
            
        if request.form.get("Saturday") == 'true':
            Saturday = True
        else:
            Saturday = False
            
        startTime = request.form.get("StartTime")
        endTime = request.form.get("EndTime")
        
        newslot = timeslots(Sunday = Sunday, Monday = Monday, Tuesday = Tuesday, Wednesday = Wednesday, Thursday = Thursday, Friday = Friday, Saturday = Saturday, startTime = startTime, endTime = endTime)
        db.session.add(newslot)
        db.session.commit()
        
        
    newslot = timeslots.query.all()
    return render_template("create.html",newslot = newslot, title = 'create')   
    
@app.route('/delete/<timeslot_id>') 
def delete(timeslot_id):
        timeslot = timeslots.query.get(timeslot_id)
        db.session.delete(timeslot)
        db.session.commit()
         
        
        timeslot = timeslots.query.all()
        return render_template("index.html",timeslot=timeslot,title ='Template')
    
@app.route('/update/<timeslot_id>', methods=['GET','POST']) 
def update(timeslot_id):
    if request.form:
        newStartTime = request.form.get("startTime")
        newEndTime = request.form.get("endTime")
         
        newM = request.form.get("Monday")
        newT = request.form.get("Tuesday")
        newW = request.form.get("Wednesday")
        newR = request.form.get("Thursday")
        newF = request.form.get("Friday")
        newS = request.form.get("Saturday")
        newSu = request.form.get("Sunday")
         
         
        timeslot = timeslots.query.get(timeslot_id)
        timeslot.startTime = newStartTime
        timeslot.endTime = newEndTime
         
        timeslot.endTime = newM
        timeslot.endTime = newT
        timeslot.endTime = newW
        timeslot.endTime = newR
        timeslot.endTime = newF
        timeslot.endTime = newS
        timeslot.endTime = newSu
         
 
        db.session.commit()
        return redirect("/")
 
    timeslot = timeslots.query.get(timeslot_id)
    return render_template("update.html",timeslot=timeslot, title = 'Update')
# this class creates a table in the database named TimeSlot with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class timeslots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Sunday = db.Column(db.Boolean, default = False)
    Monday = db.Column(db.Boolean, default = False)
    Tuesday = db.Column(db.Boolean, default = False)
    Wednesday = db.Column(db.Boolean, default = False)
    Thursday = db.Column(db.Boolean, default = False)
    Friday = db.Column(db.Boolean, default = False)
    Saturday = db.Column(db.Boolean, default = False)
    startTime = db.Column(db.String(255), default = False)
    endTime = db.Column(db.String(255), default = False)

if __name__ == '__main__':
    app.run(debug=True)
