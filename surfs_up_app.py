#import libraries 
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#create engine and automaa
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base  = automap_base()
Base.prepare(engine, reflect = True)

#declare classes
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

#set variables for start and end date
last_data_point = dt.date(2017, 8, 23)
year_from_last = last_data_point - dt.timedelta(days=365)

#defining routes 
@app.route("/")
def main():
    return(
        f"Available API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

#create query for precipitation and jsonify 
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_from_last).all()
    precip = {}
    for result in prcp_query:
        prcp_list = {result.date: result.prcp, "prcp": result.prcp}
        precip.update(prcp_list)

    return jsonify(precip)

#create api for stations query
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

#create api and query for tobs data
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_from_last).all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)

#defining queries for start and end dates 
@app.route("/api/v1.0/<start>")
def start():

    start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
            group_by(Measurement.date)

    start_list = list(start)

    return jsonify(start_list)

@app.route("/api/v1.0/<end>")
def end():
    end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= end_date).\
            group_by(Measurement.date)
    
    end_list = list(end)

    return jsonify(end_list)


if __name__ == '__main__':
    app.run(debug=True)
