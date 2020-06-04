import boto3
import yaml
import logging
logger = logging.getLogger("down_load_data")

def upload_data(args):
    """
    function to upload a data file in the local folder to a S3 bucket of user's choice
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
    except:
        logger.error("Error: upload unsuccessful.")


def download_data(args):
    """
    main function to download the raw data from a s3 bucket
    :param args (argparse): user-input configuration file
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    data_downloader(**config['run_download_data']['download_data'])


def data_downloader(bucket_name, s3_file, file_path, file_name):
    """
    Helper function to download data from a S3 bucket to the local folder based on user input
    :param bucket_name: name of the S3 bucket; default bucket is
    :param s3_file: name of the file to be downloaded
    :param file_path: path to the saved file
    :param file_name: name of the saved file
    :return: None
    """
    try:
        path = file_path + '/' + file_name
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, s3_file, path)
        logger.info("%s is downloaded from S3 bucket %s to %s " % (s3_file, bucket_name, path))
    except:
        logger.error("Error: Unable to download %s from S3 bucket %s" % (s3_file, bucket_name))

