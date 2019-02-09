import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session 
session = Session(engine)
session2 = Session(engine)
session3 = Session(engine)
session4 = Session(engine)
session5 = Session(engine)
session6 = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"I enjoyed an amazing trip to Honolulu, Hawaii and can't wait to share some of my research on the climate with you!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-08-07<br/>"
        f"/api/v1.0/2017-08-07/2017-08-19"
    )

@app.route("/api/v1.0/precipitation")
def qprcp():
    """Return a list of dates and precipitation one year from the last data point"""
    # Query 
    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= '2016-08-23').all()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations"""
    # Query all stations
    results = session2.query(Station).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def qtobs():
    """Return a list of dates and temp observations one year from the last data point for the most popular station"""
    # Query 
    results = session3.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-18').all()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/2017-08-07")
def start():
    """Return the min, avg, and max for all dates greater than the start of my trip"""
    # Query
    results = session4.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-08-07').all()

    # Convert list of tuples into normal list
    start = list(np.ravel(results))

    return jsonify(start)

@app.route("/api/v1.0/2017-08-07/2017-08-19")
def startend():
    """Return the min, avg, and max for the duration of my trip"""
    # Query
    results = session5.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-08-07').filter(Measurement.date <= '2017-08-19').all()

    # Convert list of tuples into normal list
    startend = list(np.ravel(results))

    return jsonify(startend)

if __name__ == '__main__':
    app.run(debug=True)
