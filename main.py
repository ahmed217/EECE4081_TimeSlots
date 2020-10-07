
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import re
import os

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy 

database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )

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

@app.route('/')
def index():
    timeslots = timeslots.query.all()

    return render_template(
        "index.html",
    )

@app.create('/')
def create():
    if request.form:
        Sunday = request.form.get("Sunday")
        Monday = request.form.get("Monday")
        Tuesday = request.form.get("Tuesday")
        Wednesday = request.form.get("Wednesday")
        Thursday = request.form.get("Thursday")
        Friday = request.form.get("Friday")
        Saturday = request.form.get("Saturday")
        startTime = request.form.get("Start")
        endTime = request.form.get("End")

        newslot = timeslots(Sunday = Sunday, Monday = Monday, Tuesday = Tuesday, Wednesday = Wednesday, Thursday = Thursday, Friday = Friday, Saturday = Saturday, startTime = startTime, endTime = endTime)
        db.session.add(newslot)
        db.session.commit()
        timeslots = timeslots.query.all()

    return render_template(
        "create.html",
    )




class timeslots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Sunday = db.Column(db.Boolean, nullable = False)
    Monday = db.Column(db.Boolean, nullable = False)
    Tuesday = db.Column(db.Boolean, nullable = False)
    Wednesday = db.Column(db.Boolean, nullable = False)
    Thursday = db.Column(db.Boolean, nullable = False)
    Friday = db.Column(db.Boolean, nullable = False)
    Saturday = db.Column(db.Boolean, nullable = False)
    startTime = db.Column(db.String(255), nullable = False)
    endTime = db.Column(db.String(255), nullable = False)


"""
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form.getlist('hello'))

    return '''<form method="post">
<input type="checkbox" name="Monday" value="False">
<input type="checkbox" name="hello" value="davidism">
<input type="submit">
</form>'''

app.run()
"""