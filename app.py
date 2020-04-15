from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
def home():
    """available api routes"""
    return(
        f"Climate API<br/>"
        f"Available Routes: <br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year from last data point: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/&lt;start&gt;<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session from Python to the DB
    session = Session(engine)

    #query for dates and precipitation values
    results =   session.query(measurement.date, measurement.prcp).\
                order_by(measurement.date).all()

    #convert to list of dictionaries to jsonify
    precip_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        precip_list.append(new_dict)

    session.close()

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    #create session from Python to the DB
    session = Session(engine)

    stations = {}

    #query all stations
    results = session.query(station.station, station.name).all()
    for s, name in results:
        stations[s] = name

    session.close()
 
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session from Python to the DB
    session = Session(engine)

    #get the last date contained in the dataset and date from one year ago
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_yr_ago = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #query for dates and temperature values
    results =   session.query(measurement.date, measurement.tobs).\
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

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    """TMIN, TAVG, and TMAX per date starting from a starting date.
    Args:
        start (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """

    #create session from Python to the DB
    session = Session(engine)

    return_list = []

    results =   session.query(measurement.date,\
                                func.min(measurement.tobs), \
                                func.avg(measurement.tobs), \
                                func.max(measurement.tobs)).\
                        filter(measurement.date >= start).\
                        group_by(measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):
    """TMIN, TAVG, and TMAX per date for a date range.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #create session from Python to the DB
    session = Session(engine)

    return_list = []

    results =   session.query(  Measurement.date,\
                                func.min(measurement.tobs), \
                                func.avg(measurement.tobs), \
                                func.max(measurement.tobs)).\
                        filter(and_(measurement.date >= start, measurement.date <= end)).\
                        group_by(measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

if __name__ == '__main__':
    app.run(debug=True)
