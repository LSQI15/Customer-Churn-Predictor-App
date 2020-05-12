import os
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, MetaData
import logging.config
import config
import sys
import config.flask_config as conf

logger = logging.getLogger(__name__)
Base = declarative_base()

class Customer(Base):
    """ Defines the data model for the table `customer`.
        This table will store user inputs based on which prediction will be made
    """
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)                              # auto-increment id
    Gender = Column(Integer, unique=False, nullable=False)              # binary (0/1)
    SeniorCitizen = Column(Integer, unique=False, nullable=False)       # binary (0/1)
    Partner = Column(Integer, unique=False, nullable=False)             # binary (0/1)
    Dependents = Column(Integer, unique=False, nullable=False)          # binary (0/1)
    Tenure = Column(Integer, unique=False, nullable=False)              # integer
    PhoneService = Column(Integer, unique=False, nullable=False)        # binary (0/1)
    MultipleLines = Column(Integer, unique=False, nullable=False)       # categorical with 3 classes (0/1/2)
    InternetService = Column(String(100), unique=True, nullable=False)  # categorical - company names
    OnlineSecurity = Column(Integer, unique=False, nullable=False)      # categorical with 3 classes (0/1/2)
    OnlineBackup = Column(Integer, unique=False, nullable=False)        # categorical with 3 classes (0/1/2)
    DeviceProtection = Column(Integer, unique=False, nullable=False)    # categorical with 3 classes (0/1/2)
    TechSupport = Column(Integer, unique=False, nullable=False)         # categorical with 3 classes (0/1/2)
    StreamingTV = Column(Integer, unique=False, nullable=False)         # categorical with 3 classes (0/1/2)
    StreamingMovies = Column(Integer, unique=False, nullable=False)     # categorical with 3 classes (0/1/2)
    Contract = Column(String(100), unique=True, nullable=False)         # categorical - contact type
    PaperlessBilling = Column(Integer, unique=False, nullable=False)    # binary (0/1)
    PaymentMethod = Column(String(100),  unique=True, nullable=False)   # categorical - payment type
    MonthlyCharges = Column(sql.Float, unique=False, nullable=False)    # double
    TotalCharges = Column(sql.Float, unique=False, nullable=False)      # double

    def __repr__(self):
        return "<Customer(id='%d', monthly_charges='%d', total_charges='%d')>" \
               % (self.id, self.MonthlyCharges, self.TotalCharges)


def create_db(args):
    """
        Create the database locally or in RDS based on user input
        :param args: True/False indicating whether to create the database in RDS
        :return: None
    """
    if args.rds == "True":      # set up the database in RDS
        engine_string = conf.RDS_ENGINE_STRING
    elif args.rds == "False":   # set up the database locally
        engine_string = conf.LOCAL_ENGINE_STRING
    else:
        raise logger.error("Invalid args.rds option %s: " % args.rds)
    # create engine and database
    engine = sql.create_engine(engine_string, echo = True)
    Base.metadata.create_all(engine)