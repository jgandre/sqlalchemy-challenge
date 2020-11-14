from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import and_, extract
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt
from flask import Flask, jsonify, request
#from flask import sqlalchemy

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
engine =  create_engine(f"sqlite:///{database_path}")
conn = engine.connect()
session = Session(bind=engine)

#find max date
# max_date = session.query(func.max(M.date)).first()[0]

# one_year_ago = max_date - timedelta(days=365)

# my_data = session.query(M).filter(M.date >= one_year_ago,  M.date <= max_date)

# all_info_df = pd.read_sql(my_data.statement, my_data.session.bind)

# my_data = session.query(M.prcp, M.date).filter(M.date >= one_year_ago,  M.date <= max_date)

# pprint(type(my_data))
# pprint(my_data)

# prcp_date_df = pd.read_sql(my_data.statement, my_data.session.bind)
# prcp_date_df

# index_prcp_date_df = pd.read_sql(my_data.statement, my_data.session.bind).set_index("date")
# index_prcp_date_df.head(25)my_data = session.query(M.prcp, M.date).filter(M.date >= one_year_ago,  M.date <= max_date)

def test ():
    return "Hello work"


def test2():

#find max date

    max_date = session.query(func.max(M.date)).first()[0]
    pprint(max_date)
    one_year_ago = max_date - timedelta(days=365)
    one_year_ago
    my_data = session.query(M).filter(M.date >= one_year_ago,  M.date <= max_date)
    print (str(my_data))
    return str(my_data)

@app.route("/")
def welcome():
    return work.test2()
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def recent_yr_prcp ():
    max_date = session.query(func.max(M.date)).first()[0]
    date_time_obj = dt.datetime.strptime(max_date, '%Y-%m-%d')
    one_year_ago = date_time_obj - timedelta(days=365)
    one_year_ago_query = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date).all()
    prcp = list(np.ravel(one_year_ago_query))
    
    print (f"Below is the precipation value by date")
    return jsonify (precipitation = prcp)
    
@app.route("/api/v1.0/station-count")
def stations():
    station_count = str(session.query(station).count())
      return ("There are: " + " " + station_count + " " + "stations.")
    
    
@app.route("/api/v1.0/stations")
def stations():
    station = session.query(M.station, 
    func.count(M.id))
    .group_by(M.station)
    .order_by(func.count(M.station).desc()).all()
    station_list = list(station)
    print(f"The most active stations are:")
    return jsonify(station_list)


 
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
def popular_station():
    max_date = session.query(func.max(M.date)).first()[0]
    date_time_obj = dt.datetime.strptime(max_date, '%Y-%m-%d')
    one_year_ago = date_time_obj - timedelta(days=365)
    recent_yr_most_active = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date).filter(func.max(M.station)).all()
    tobs_most_active = list(np.ravel(recent_yr_most_active)
    
    return jsonify(tobs = tobs_most_active)
     
#another optin for above with direct input of station and dates 
                            
def tobs():
    tobs = session.query(M.date, M.tobs).filter(Measurement.station=="USC00519281").filter
    (and_(M.date >= "2016-08-23", M.date <= "2017-08-23")).all()
    tobs_list = list(tobs)
    return jsonify(tobs_list)

                            
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.    
    
@app.route("/api/v1.0/<start>")
def start_date(start):
    start = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).filter(M.date >= start).all()
    return jsonify (start_date = start)
                            
                                                       
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
   date_range = session.query(func.min(M.tobs), func.avg(M.tobs),func.max(M.tobs)).filter(M.date.between(start, end)).all()
        return jsonify(date_range)

if __name__ == "__main__":
    app.run(debug=True)