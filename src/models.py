from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestTable(Base):
    __tablename__ = "testtable"

    id = Column(Integer, primary_key=True)
    city = Column(String(255))
    lat = Column(Float)
    date = Column(Date)

