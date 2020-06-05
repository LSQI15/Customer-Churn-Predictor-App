import argparse
import logging.config

from config.flaskconfig import LOGGING_CONFIG
logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


from src.upload_download_data import upload_data, download_data
from src.data_preprocess import preprocess_data
from src.featurize import feaurize
from src.eda import eda
from src.model_training import random_forest
from src.model_evaluation import evaluate_model
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.customer_db import create_db, initial_ingest
from test.reproducibility_test import run_reproducibility_tests


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run Components of Model Source Code")
    subparsers = parser.add_subparsers()

    # Sub-parser for downloading raw data from S3 bucket
    sb_download = subparsers.add_parser("download_data", description="Download data from S3 bucket")
    sb_download.add_argument('--config', help='path to yaml file with configurations')
    sb_download.set_defaults(func=download_data)

    # Sub-parser for cleaning raw data
    sb_preprocess = subparsers.add_parser("preprocess_data", description="Clean the raw data")
    sb_preprocess.add_argument('--config', help='path to yaml file with configurations')
    sb_preprocess.set_defaults(func=preprocess_data)

    # Sub-parser for featurizing preprocessed data
    sb_feature = subparsers.add_parser("feaurize", description="featurize the preprocessed data")
    sb_feature.add_argument('--config', help='path to yaml file with configurations')
    sb_feature.set_defaults(func=feaurize)

    # Sub-parser for exploratory data analysis
    sb_eda = subparsers.add_parser("eda", description="exploratory data analysis")
    sb_eda.add_argument('--config', help='path to yaml file with configurations')
    sb_eda.set_defaults(func=eda)

    # Sub-parser for training random forest model
    sb_random_forest = subparsers.add_parser("random_forest", description="training random forest model")
    sb_random_forest.add_argument('--config', help='path to yaml file with configurations')
    sb_random_forest.set_defaults(func=random_forest)

    # Sub-parser for evaluating the random forest model
    sb_eval = subparsers.add_parser("evaluate_model",
                                        description="evaluate the model and save evaluations in .csv files")
    sb_eval.add_argument('--config', help='path to yaml file with configurations')
    sb_eval.set_defaults(func=evaluate_model)

    # Sub-parser for creating a database to store user input
    sb_create_db = subparsers.add_parser("create_db", description="Creating the Databse")
    sb_create_db.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")
    sb_create_db.set_defaults(func=create_db)

    # Sub-parser for conducting initial ingestion to the database
    sb_init_ingest = subparsers.add_parser("initial_ingest", description="Initial ingestion to the Databse")
    sb_init_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                              help="SQLAlchemy connection URI for database")
    sb_init_ingest.add_argument('--config', help='path to yaml file with configurations')
    sb_init_ingest.add_argument('--num_records', default=5, help='the number of records to ingest')
    sb_init_ingest.set_defaults(func=initial_ingest)

    # Sub-parser for conducting reproducibility test
    sb_reproducibility_test = subparsers.add_parser("run_reproducibility_tests", description="Run reproducibility tests")
    sb_reproducibility_test.add_argument('--config', help='path to yaml file with configurations')
    sb_reproducibility_test.set_defaults(func=run_reproducibility_tests)

    # Sub-parser for uploading the data to S3 bucket
    sb_upload = subparsers.add_parser("upload_data", description="Upload data into S3")
    sb_upload.add_argument('--local_file_path', help="Local folder containing data to be uploaded")
    sb_upload.add_argument('--file_name', help="File name of the data file")
    sb_upload.add_argument('--bucket_name', help="AWS S3 bucket where the data will be stored")
    sb_upload.set_defaults(func=upload_data)

    args = parser.parse_args()
    args.func(args)
