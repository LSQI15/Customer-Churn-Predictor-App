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
LOCAL_DATABASE_URI = 'sqlite:////{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# RDS Database Connection Config

