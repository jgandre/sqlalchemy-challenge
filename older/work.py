from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import and_, extract
from datetime import datetime, timedelta
import pandas as pd


from pprint import pprint

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


# all_info_df = pd.read_sql(my_data.statement, my_data.session.bind)
# all_info_df

# my_data = session.query(M.prcp, M.date).filter(M.date >= one_year_ago,  M.date <= max_date)

# pprint(type(my_data))
# pprint(my_data)

# prcp_date_df = pd.read_sql(my_data.statement, my_data.session.bind)
# prcp_date_df

# index_prcp_date_df = pd.read_sql(my_data.statement, my_data.session.bind).set_index("date")
# index_prcp_date_df.head(25)


# prcp_date_df.describe()

# # ### Station Analysis

# # * Design a query to calculate the total number of stations.
# station_count = session.query(func.count(Stations.id)).first()[0]
# print(station_count)
# print(f"The total number of stations is {station_count}.")
# print("-----------------------------------------------------")
# # *Design a query to find the most active stations.
# station_activity_count = session.query(M.station, func.count(M.station)).group_by(M.station).all()
# print(station_activity_count)

# s_activity = pd.read_sql("SELECT station, count(station) FROM measurement GROUP BY station" , conn)
# most_active_station_df = s_activity.sort_values(by=['count(station)'], ascending = False)
# one = most_active_station_df['station'][6]
# two = most_active_station_df['station'][7]
# three = most_active_station_df['station'][1]

# print("-----------------------------------------------------")

# most_active_station = session.query(func.max(M.station)).first()[0]

# #print(most_active_station)
# print(f"The most active station is {most_active_station}.")
# print(f"The 3 most active stations in order by station name are {one}, {two}, {three}" )

# print("-----------------------------------------------------")

# most_active_station_df

# #Design a query to retrieve the last 12 months of temperature observation data (TOBS).
# recent_yr_tobs = session.query(M.tobs, M.date).filter(M.date >= one_year_ago,  M.date <= max_date)

# tobs_df = pd.read_sql(recent_yr_tobs.statement, recent_yr_tobs.session.bind)
# tobs_df

# # Filter by the station with the highest number of observations: Includes TOBS plus date and station name.
# my_data = session.query(M.tobs, M.date, M.station).filter(M.date >= one_year_ago,  M.date <= max_date, M.station == 'USC00519523')

# most_active_station_tobs_df = pd.read_sql(my_data.statement, my_data.session.bind)
# most_active_station_tobs_df

# # Filter by the station with the highest number of observations: Includes only TOBS.
# my_data = session.query(M.tobs).filter(M.date >= one_year_ago,  M.date <= max_date, M.station == 'USC00519523')

# most_active_station_tobs_df = pd.read_sql(my_data.statement, my_data.session.bind)
# most_active_station_tobs_df