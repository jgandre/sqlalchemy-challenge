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


if __name__ == "__main__":
    app.run(debug=True)