from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import and_, extract
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
#from matplotlib import pyplot as plt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )

#find max date

    #prcp = list(np.ravel(prcps))

#Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
@app.route("/api/v1.0/precipitation")
def recent_yr_prcp_dict():

    max_date = session.query(func.max(M.date)).first()[0]
    one_year_ago = max_date - timedelta(days=365)
    dates = session.query(M.date).filter(M.date >= one_year_ago,  M.date <= max_date)
    date_str = str(dates)
    prcps = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date)
    prcp = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date).all()

    prcp_dict = {date: recent_yr_prcp_dict for str(date), recent_yr_prcp_dict in prcp}
    return jsonify(prcp_dict)




    #ps = session.query(M.date, M.prcp).filter(M.date >= "2016-08-23").filter(M.date <= "2017-08-23").all()
    # max_date = session.query(func.max(M.date)).first()[0]
    # one_year_ago = max_date - timedelta(days=365)
    # dates = session.query(M.date).filter(M.date >= one_year_ago,  M.date <= max_date)
    # date_str = str([dates])
    # prcps = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date)
    # prcp_dict = {date_str: precipitation for date_str, precipitation in prcps}
    # return jsonify(prcp_dict)


    # max_date = session.query(func.max(M.date)).first()[0]
    # one_year_ago = max_date - timedelta(days=365)
    # dates = session.query(M.date).filter(M.date >= one_year_ago,  M.date <= max_date)
    # date_str = str(dates)
    # prcps = session.query(M.date, M.prcp).filter(M.date >= one_year_ago,  M.date <= max_date)
    

    

    # for prcp in prcps.all():
    #     return ({dates: prcps})
    #    # def object_as_dict(obj):
    # #return {c.key: getattr(obj, c.key)
    # #        for c in inspect(obj).mapper.column_attrs}

#query = session.query(User)
    #for prcp in prcps:
      #  return(prcp)
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
