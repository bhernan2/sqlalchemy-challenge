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
    #convert dictionaries to jsonify
    precip_dates = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
    session.close()

    return jsonify(precip_dates)
@app.route("/api/v1.0/stations")
def stations():
    #create session link from Python to DB
    session = Session(engine)
    stations = {}
    #query all stations
    results = session.query(station.station, station.name).all()
    for s, name in results: 
        stations[s] = name

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def stations():
    #create session link from Python to DB
    session = Session(engine)
    #get last date and date from one year ago
    last_date = session.query(measurement.date, measurement.tobs).order_by(measurement.date.desc()).first()
    one_yr_ago = (dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")
    #query for dates and temperatures
    results = session.query(measurement.date, measurement.tobs).\
              filter(measurement.date >= one_yr_ago).\
              order_by(measurement.date).all()
    
    #convert dictionaries to jsonify
    date_tobs = []

    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        date_tobs.append(new_dict)
    session.close()

    return jsonify(date_tobs)

if __name__ == '__main__':
    app.run(debug=True)      


            


