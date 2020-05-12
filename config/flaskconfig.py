import os
import sys

# get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging Config
LOGGING_CONFIG = os.path.join(PROJECT_ROOT, 'config/logging/local.conf')

# App Config
APP_NAME = "customer_churn"
DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Local Sqlite Database Connection Config
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'data/customer.db')
LOCAL_ENGINE_STRING = 'sqlite:////{}'.format(DATABASE_PATH)

# RDS Database Connection Config
# the engine_string format
# engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}"
CONN_TYPE = "mysql+pymysql"
RDS_USER = os.environ.get("MYSQL_USER")
RDS_PASSWORD = os.environ.get("MYSQL_PASSWORD")
RDS_HOST = os.environ.get("MYSQL_HOST")
RDS_PORT = os.environ.get("MYSQL_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
RDS_ENGINE_STRING = "{}://{}:{}@{}:{}/{}".\
format(CONN_TYPE, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_PORT, DATABASE_NAME)

# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
# if SQLALCHEMY_DATABASE_URI is not None:
#     pass
# elif RDS_HOST is None:
#     SQLALCHEMY_DATABASE_URI = LOCAL_ENGINE_STRING
# else:
#     SQLALCHEMY_DATABASE_URI = RDS_ENGINE_STRING