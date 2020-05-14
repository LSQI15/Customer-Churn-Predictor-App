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
        local_file_path: path to the saved file
        file_name: the name of the file
        bucket_name: link to the S3 bucket
    :return: None
    """
    s3 = boto3.client('s3')
    try:
        path = args.local_file_path + '/' + args.file_name
        s3.upload_file(path, args.bucket_name, 'data/%s' % args.file_name)
        logger.info("%s is successfully uploaded to bucket %s" % (args.file_name, args.bucket_name))
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Error: upload unsuccessful.")


def download_data(args):
    """
    Download data from a public S3 bucket to the local folder based on user input
    :param args
        .bucket_name (String): name of the S3 bucket; default bucket is 'msia423-customer-churn'
        .s3_file: file to be downloaded; default is 'data/raw_data.csv'
        .local_file_path (String): path to the saved file
        .file_name (String): name of the file
    :return: None
    """
    path = args.local_file_path + '/' + args.file_name
    try:
        s3 = boto3.client('s3')
        s3.download_file(args.bucket_name, args.s3_file, path)
        logger.info("%s is downloaded from S3 bucket %s to %s " % (args.s3_file, args.bucket_name, path))
    except requests.exceptions.RequestException:
        logger.error("Error: Unable to download %s from S3 bucket %s" % (args.s3_file, args.bucket_name))

