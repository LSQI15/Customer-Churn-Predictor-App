import argparse

from src.create_db import create_db
from src.upload_download_data import upload_data, download_data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run Components of Model Source Code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database to store user input
    sb_create_db = subparsers.add_parser("create_db", description="Creating the Databse")
    sb_create_db.add_argument('--rds', default="False", help='Option to use RDS or not')
    sb_create_db.set_defaults(func=create_db)

    # Sub-parser for downloading raw data from S3 bucket
    sb_download = subparsers.add_parser("download_data", description="Download data from S3 bucket")
    sb_download.add_argument('--local_file_path', default="data", help="Local folder where downloaded data will be saved")
    sb_download.add_argument('--file_name', default="customer_churn.csv", help="File name of the data file")
    sb_download.add_argument('--bucket_name', default="msia423-customer-churn", help="AWS S3 bucket where the data is stored")
    sb_download.add_argument('--s3_file', default="data/raw_data.csv", help="File to be downloaded")
    sb_download.set_defaults(func=download_data)

    # Sub-parser for uploading the data to S3 bucket
    sb_upload = subparsers.add_parser("upload_data", description="Upload data into S3")
    sb_upload.add_argument('--local_file_path', default="data", help="Local folder containing data to be uploaded")
    sb_upload.add_argument('--file_name', default="raw_data.csv", help="File name of the data file")
    sb_upload.add_argument('--bucket_name', help="AWS S3 bucket where the data will be stored")
    sb_upload.set_defaults(func=upload_data)

    args = parser.parse_args()
    args.func(args)
