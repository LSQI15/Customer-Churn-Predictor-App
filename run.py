import argparse

from src.create_db import create_db
from src.upload_download_data import upload_data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run Components of Model Source Code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create_db = subparsers.add_parser("create_db", description="Creating the Databse")
    sb_create_db.add_argument('--rds', default=False, help='Option to use RDS or not')
    sb_create_db.set_defaults(func=create_db)

    # Sub-parser for uploading the data to S3
    sb_upload = subparsers.add_parser("upload_data", description="Upload data into S3")
    sb_upload.add_argument('--localfolder', help="Local folder containing data to be uploaded")
    sb_upload.add_argument('--filename', help="File name of the data file")
    sb_upload.add_argument('--bucket', help="AWS S3 bucket where the data will be stored")
    sb_upload.set_defaults(func=upload_data)

    args = parser.parse_args()
    args.func(args)
