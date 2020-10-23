
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import re
import os
import pytest



# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy 
"""
database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )
    """

database = "sqlite:///timeSlots.db"
#{{ timeSlots.daysOfWeek }} {{ timeSlots.startTime }} {{ timeSlots.startTimeAMPM }} - {{ timeSlots.endTime }} {{ timeSlots.endTimeAMPM  }}
app = Flask(__name__)
app.secret_key = 'test'
# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)

#@app.route('/init_db')
#def init_db():
#    db.drop_all()
#    db.create_all() 
#    return 'DB initialized'

#def test_index(client):
    #Main page shows a welcome message.
    #main_page = client.get('/')
    #assert b'This is an application to manage Broken Laptops' in main_page.data
    #assert b'Hello, world!' in main_page.data
    #assert b'brand in main_page.data
    #assert b'prince' in main_page.data

    # Routes to home page
@app.route('/') 
@app.route('/index')
def index():
    timeslot = timeSlots.query.all()
    return render_template("home.html",timeslot=timeslot, year=datetime.now().year, title = 'Home')


    # Routes to timeslots page
@app.route('/') 
@app.route('/timeslots')
def timeslots():
    timeslot = timeSlots.query.all()
    return render_template("index.html",timeslot=timeslot, year=datetime.now().year, title = 'Timeslots')

    # Creates entries in the database
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        daysOfWeek = ''
        if request.form:
            if request.form.get("Sunday") == 'true':
                    daysOfWeek += 'U'

        if request.form:
            if request.form.get("Monday") == 'true':
                    daysOfWeek += 'M'

        if request.form:
            if request.form.get("Tuesday") == 'true':
                    daysOfWeek += 'T'

        if request.form:
            if request.form.get("Wednesday") == 'true':
                    daysOfWeek += 'W'

        if request.form:
            if request.form.get("Thursday") == 'true':
                    daysOfWeek += 'R'

        if request.form:
            if request.form.get("Friday") == 'true':
                    daysOfWeek += 'F'

        if request.form:
            if request.form.get("Saturday") == 'true':
                    daysOfWeek += 'S'
            
            startTime = request.form.get("StartTime")
            startTime_AMPM = request.form.get("startTime_AMPM")
            endTime = request.form.get("EndTime")
            endTime_AMPM = request.form.get("endTime_AMPM")
            newslot = timeSlots(daysOfWeek = daysOfWeek, startTime = startTime, startTime_AMPM = startTime_AMPM, endTime = endTime, endTime_AMPM = endTime_AMPM)
            db.session.add(newslot)
            db.session.commit()
            timeslot = timeSlots.query.all()
            return render_template("index.html",timeslot=timeslot, year=datetime.now().year, title = 'Timeslots')
        
    
        # Deletes entries in the database
@app.route('/delete/<timeslot_id>') 
def delete(timeslot_id):
        timeslot = timeSlots.query.get(timeslot_id)
        db.session.delete(timeslot)
        db.session.commit()
        timeslot = timeSlots.query.all()
        return render_template("index.html", year=datetime.now().year, timeslot=timeslot,title ='Timeslots')


       # Updates entries in the database
@app.route('/update', methods = ['GET', 'POST'])
def update():
        if request.method == 'POST':
            daysOfWeek = ''
            if request.form:
                if request.form.get("Sunday") == 'true':
                        daysOfWeek += 'U'

            if request.form:
                if request.form.get("Monday") == 'true':
                        daysOfWeek += 'M'

            if request.form:
                if request.form.get("Tuesday") == 'true':
                        daysOfWeek += 'T'

            if request.form:
                if request.form.get("Wednesday") == 'true':
                        daysOfWeek += 'W'

            if request.form:
                if request.form.get("Thursday") == 'true':
                        daysOfWeek += 'R'

            if request.form:
                if request.form.get("Friday") == 'true':
                        daysOfWeek += 'F'

            if request.form:
                if request.form.get("Saturday") == 'true':
                        daysOfWeek += 'S'

            my_data = timeSlots.query.get(request.form.get('id'))
            my_data.startTime = request.form['startTime']
            my_data.startTime_AMPM = request.form['startTime_AMPM']
            my_data.endTime = request.form['endTime']
            my_data.endTime_AMPM = request.form['endTime_AMPM']
            my_data.daysOfWeek = daysOfWeek
            db.session.commit()
            timeslot = timeSlots.query.all()
            return render_template("index.html", year=datetime.now().year, timeslot=timeslot, title = 'Timeslots') 

        return render_template("index.html", year=datetime.now().year, timeslot=timeslot, title = 'Timeslots') 


    # Routes to the about page
@app.route('/about')
def about():
        return render_template(
            'about.html',
            title='About',
            year=datetime.now().year,
            message='This application was developed for a class assignment in EECE 4081'
        )


# this class creates a table in the database named TimeSlot with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class timeSlots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    daysOfWeek = db.Column(db.String(255), nullable = False)
    startTime = db.Column(db.String(255), nullable = False)
    startTime_AMPM = db.Column(db.String(255), nullable = False)
    endTime = db.Column(db.String(255), nullable = False)
    endTime_AMPM = db.Column(db.String(255), nullable = False)

#if __name__ == '__main__':
#    app.run(debug=True)


# Added this code for visual studios
# Not needed in google app engine
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)