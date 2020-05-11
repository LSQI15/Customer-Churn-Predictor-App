import boto3
import requests
import yaml
import argparse
import os

import logging
logger = logging.getLogger(__name__)

def upload_data(args):
    """
    Upload data in the local folder to a S3 bucket of user's choice
    :param args: The name of S3 bucket which data will be uploaded to
    :return: None
    """
    s3 = boto3.client('s3')
    try:
        filepath = args.localfolder + '//' + args.filename
        s3.upload_file(filepath, args.bucket, 'data/%s' % args.filename)
        logger.info("%s is successfully uploaded to bucket %s" % (args.filename, args.bucket))
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Error: upload unsuccessful.")


def download_data(file_name, source_url, local_file_path):
    """
    Download data from a public S3 bucket to the local folder based on user input
    :param file_name (String): name of the file
    :param source_url (String): link to the S3 bucket
    :param local_file_path (String): path to the saved file
    :return: None
    """


