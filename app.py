#setting up dependenices
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#===set up database===
#create engine to databse
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect database to a new base
Base = automap_base()
#reflect the tables
Base.prepare(engine,reflect=True)
#save tables into references
Mfake = Base.classes.measurement
Sfake = Base.classes.station

#===flask coding===
#generate app instance
app = Flask(__name__)

#define app and details

@app.route('/')
def homepage():

