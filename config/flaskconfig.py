import os
import sys

# get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging Config
LOGGING_CONFIG = os.path.join(PROJECT_ROOT, 'config/logging/local.conf')

# App Config
APP_NAME = "customer_churn"
DEBUG = True

# Local Sqlite Database Connection Config
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'data/customer.db')
LOCAL_ENGINE_STRING = 'sqlite:////{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# RDS Database Connection Config
# the engine_string format
# engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}"
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
RDS_HOST = os.environ.get("MYSQL_HOST")
RDS_PORT = os.environ.get("MYSQL_PORT")
DATABASE_NAME = os.environ.get("MYSQL_DATABASE_NAME")
RDS_ENGINE_STRING = "{}://{}:{}@{}:{}/{}".\
format(CONN_TYPE, USER, PASSWORD, RDS_HOST, RDS_PORT, DATABASE_NAME)

