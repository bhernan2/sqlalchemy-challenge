import numpy as numpy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement 
Station = Base.classes.station 

#set up flask
app = Flask(_name_)

#set up flask routes: /, /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/<start> and /api/v1.0/<start>/<end>
  
