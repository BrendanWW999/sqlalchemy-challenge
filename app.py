


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
station = Base.classes.station
measurement = Base.classes.measurement

app = Flask(__name__)

start_date = '2016-01-01'
end_date = '2016-01-07'

@app.route("/")
def home():
    print("All available api routes")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend<br/>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results_1 = session.query(measurement.date, measurement.prcp).all()
    session.close()
    prcpdata_1 = []
    for date, prcp in results_1:
        prcpdata = {}
        prcpdata["date"] = date
        prcpdata["prcp"] = prcp
        prcpdata_1.append(prcpdata)

    return jsonify(prcpdata_1)
    
@app.route("/api/v1.0/stations")
def station_1():

    session = Session(engine)
    stations_1 = session.query(station.station).all()
    session.close()
    stationlist = list(np.ravel(stations_1))
    return jsonify(stationlist)
   
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    tobs_1 = session.query(measurement.tobs).filter(measurement.date >= '2016-08-24', measurement.station == 'USC00519397').order_by(measurement.tobs).all() 
    session.close()
    tobslist = list(np.ravel(tobs_1))
    return jsonify(tobslist)
    
@app.route("/api/v1.0/start")
def start():

    session = Session(engine)
    start_1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    session.close()
    startlist = list(np.ravel(start_1))
    return jsonify(startlist)

@app.route("/api/v1.0/startend")    
def startend():

    session = Session(engine)
    startend_1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()
    startendlist = list(np.ravel(startend_1))
    return jsonify(startendlist)

if __name__ == '__main__':
    app.run(debug=True)