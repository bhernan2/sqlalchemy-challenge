import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
#Database setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect tables
Base.prepare(engine, reflect=True)

#save reference to the table
measurement = Base.classes.measurement
station=Base.classes.station

#################################################
#Flask setup
#################################################
app = Flask(__name__)

#################################################
#Flask routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Temperature start date(yyyy-mm-dd): /api/v1.0/<start>"
        f"Temperature strat to end dates (yyyy-mm-dd): /api/v1.0/<start>/<end>"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link from Python to DB
    session = Session(engine)
    #query for dates and precipitation 
    results = session.query(measurement.date, measurement.prcp).\
              order_by(measurement.date).all()
    #convert to dictionaries to jsonify
    precip_dates = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
    session.close()

    return jsonify(precip_dates)
    


            


