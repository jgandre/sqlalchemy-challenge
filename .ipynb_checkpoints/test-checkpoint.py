from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import and_, extract

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

#find max date
max_date = session.query(func.max(M.date)).first()[0]
pprint(max_date)

#one year from max date
one_year_ago = max_date - timedelta(days=365)
print(one_year_ago)


my_data = session.query(M).filter(M.date >= one_year_ago,  M.date <= max_date)

pprint(type(my_data))

#ORM query object read it into a dataframe
testdf = pd.read_sql(my_data.statement, my_data.session.bind)
testdf


q_result = session.query(M).limit(10)
print(q_result)

# #shows the info in dict format ... 2 options below (DON"T NEED FOR HW)
# for row in q_result:
#     print(row)
#     pprint(row.__dict__)
    
# pprint([row.__dict__ for row in query.all()])

#print lenth of query
#print(len(query.all()))

#find max date
q = session.query(func.max(M.date))
pprint(q.first())

# find average close price in February
q = session.query(M).filter(
    and_(M.date > "2016-08-24", M.date < "2017-08-23")).first()
pprint(q)