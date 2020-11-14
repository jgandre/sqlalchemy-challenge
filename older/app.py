from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import and_, extract
import timedelta as dt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
import sqlalchemy

from pprint import pprint

app = Flask(__name__)

Base = declarative_base()

class M(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)

class Stations(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    
database_path = "Resources/hawaii.sqlite"
engine =  create_engine(f"sqlite:///{database_path}",connect_args={"check_same_thread": False})
conn = engine.connect()
session = Session(bind=engine)


@app.route("/")
def welcome():
    
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )


@app.route("/api/v1.0/precipitation")
def recent_yr_prcp ():
    max_date = session.query(func.max(M.date)).first()[0]
    #date_time_obj = dt.datetime.strptime(max_date, '%Y-%m-%d')
    max_string_date = max_date.strftime("%Y-%m-%d")
    one_year_ago = max_date - timedelta(days=365)
    string_date = one_year_ago.strftime("%Y-%m-%d")
    #one_year_ago_query = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date).all()
    one_year_ago_query = session.query(M.date, M.prcp).filter(M.date >= string_date,  M.date <= max_string_date).all()
    prcp = list(np.ravel(one_year_ago_query))
        
    print(f"Below is the past 12 months precipation value by date")
    return jsonify (precipitation = prcp)
    
@app.route("/api/v1.0/station-count")
def station_count():
    station_count = str(session.query(station).count())
    return ("There are: " + " " + station_count + " " + "stations.")
    
#Return a JSON list of stations from the dataset.  
@app.route("/api/v1.0/stations")
def stations():
    # station = session.query(M.station, 
    # func.count(M.id)).group_by(M.station).order_by(func.count(M.station).desc()).all()
    # station_list = list(station)
    station = session.query(Stations.name, Stations.station)
    station_list = list(station)
    
    return jsonify(station_list)


 
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def popular_station():
    max_date = session.query(func.max(M.date)).first()[0]
    max_string_date = max_date.strftime("%Y-%m-%d")
    one_year_ago = max_date - timedelta(days=365)
    string_date = one_year_ago.strftime("%Y-%m-%d")
    recent_yr_most_active = session.query(M.date, M.tobs).filter(M.date >= string_date,  M.date <= max_string_date).filter().all()
    tobs_most_active = list(np.ravel(recent_yr_most_active))
    return jsonify(tobs = tobs_most_active)

                            
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.    
    
@app.route("/api/v1.0/<start>")
def start_date(start=None):
    start_date = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).filter(M.date >= start).all()
    return jsonify (start_date = start_date)
                            
  #When given the start and the end date, calculate the `TMIN`, `TAVG`, and
  # `TMAX` for dates between the start and end date inclusive.                                                      
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    query = session.query(func.min(M.tobs), func.avg(M.tobs),func.max(M.tobs))

    if start:
        query = query.filter(M.date >= start)
    if end:
        query = query.filter(M.date <= end)
    q_result = query.all()
    q_result_list = list(q_result)
    return jsonify(q_result_list)

if __name__ == "__main__":
    app.run(debug=True)