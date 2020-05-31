import sqlalchemy as sql
import logging.config
import yaml
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from src.helper import csv_reader, load_model, make_ingest_df

logger = logging.getLogger(__name__)
Base = declarative_base()

class Customer(Base):
    """ Defines the data model for the table `customer`.
        This table will store user inputs based on which prediction will be made
    """
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)                               # auto-increment id
    Gender = Column(String(100), unique=False, nullable=False)          # binary (Yes/No)
    SeniorCitizen = Column(String(100), unique=False, nullable=False)    # binary (Yes/No)
    Partner = Column(String(100), unique=False, nullable=False)          # binary (Yes/No)
    Dependents = Column(String(100), unique=False, nullable=False)       # binary (Yes/No)
    Tenure = Column(Float, unique=False, nullable=False)                 # double
    PhoneService = Column(String(100), unique=False, nullable=False)     # binary (Yes/No)
    MultipleLines = Column(String(100), unique=False, nullable=False)    # categorical with 3 classes ('No phone service', 'No', 'Yes')
    InternetService = Column(String(100), unique=False, nullable=False)  # categorical with 3 classes ('DSL', 'Fiber optic', 'No')
    OnlineSecurity = Column(String(100), unique=False, nullable=False)   # binary (Yes/No)
    OnlineBackup = Column(String(100), unique=False, nullable=False)     # binary (Yes/No)
    DeviceProtection = Column(String(100), unique=False, nullable=False) # binary (Yes/No)
    TechSupport = Column(String(100), unique=False, nullable=False)      # binary (Yes/No)
    StreamingTV = Column(String(100), unique=False, nullable=False)      # binary (Yes/No)
    StreamingMovies = Column(String(100), unique=False, nullable=False)  # binary (Yes/No)
    Contract = Column(String(100), unique=False, nullable=False)         # categorical with 3 classes ('Month-to-month', 'One year', 'Two year')
    PaperlessBilling = Column(String(100), unique=False, nullable=False) # binary (Yes/No)
    PaymentMethod = Column(String(100), unique=False, nullable=False)    # categorical with 4 classes ('Electronic check', 'Mailed check','Bank transfer (automatic)','Credit card (automatic)'
    MonthlyCharges = Column(Float, unique=False, nullable=False)         # double
    TotalCharges = Column(Float, unique=False, nullable=False)           # double
    PredProbability = Column(Float, unique=False, nullable=False)        # double
    PredClass = Column(String(100), unique=False, nullable=False)        # binary (Yes/No)

    def __repr__(self):
        return "<Customer(id='%d', monthly_charges='%d', total_charges='%d')>" \
               % (self.id, self.MonthlyCharges, self.TotalCharges)


def create_db(args):
    """
    Create the database locally or in RDS
    :param args: Argparse args - should include args.engine_string
    :return: None
    """
    try:
        engine = sql.create_engine(args.engine_string, echo = True)
        Base.metadata.create_all(engine)
        logger.info("Database has been successfully created at %s" % args.engine_string)
    except:
        logger.error("Error: unable to create database at %s" % args.engine_string)


def ingest_db(df, engine_string):
    """
    helper function to add records to the existing database based on a data frame
    :param df: a pandas data frame ready to be ingested to the database
    :param engine_string: engine string of the database
    :return: None
    """
    try:
        df.to_sql(con=engine_string, index=False, name=Customer.__tablename__, if_exists='append')
        logger.info('Successfully ingested records to the database.')
    except:
        logger.error('Error: unable to ingest records to the database')


def initial_ingest(args):
    """
    main function to conduct initial ingestion to the database
    :param args: Argparse args - should include args.engine_string, args.config
    :return: None
    """
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        # load the random forest model
        rf = load_model(**config['run_create_db']['init_ingest'])
        # add all existing records in the preprocessed data to the database
        df = csv_reader(**config['run_create_db']['init_df']).drop('Churn', axis=1)
        # make a data frame that is ready for ingestion
        ingest_df = make_ingest_df(rf, df)
        # add customers to the database.
        ingest_db(ingest_df, args.engine_string)
    except:
        logger.error('Error: unable to conduct initial ingestion to the database')

