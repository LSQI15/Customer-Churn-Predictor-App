import yaml
import numpy as np
import logging

logger = logging.getLogger(__name__)
from src.helper import csv_reader, df_to_csv


def preprocess_data(args):
    """
    main function to preprocess/clean the raw data
    :param args (argparse): user-input configuration file
    """
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        df = csv_reader(**config['run_preprocess_data']['read_csv'])
        # 1. process TotalCharges column - convert spaces to NaN and drop 11 missing values
        df = TotalCharges_processor(df)
        # 2 process SeniorCitizen column - convert to binary Yes/No
        df = SeniorCitizen_processor(df)
        # 3 replace 'No internet service' to 'No' for the following 6 columns 'OnlineSecurity', 'OnlineBackup',
        # 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
        df = No_internet_service_converter(df, **config['run_preprocess_data']['internet'])
        # 4 drop the id column
        df = drop_customerID(df)
        # export preprocessed data to a csv file
        df_to_csv(df, **config['run_preprocess_data']['save_csv'])
    except:
        logger.error("Error: unable to preprocess the raw data")


def TotalCharges_processor(df):
    """
    helper function to clean the column TotalCharges
    :param df: a pandas data frame contains the raw data
    :return processed_df: a pandas data frame with 'TotalCharges' column processed.
    """
    try:
        processed_df = df
        # replace spaces with NaN in the TotalCharges column
        processed_df['TotalCharges'] = processed_df["TotalCharges"].replace(" ", np.nan).astype(float)
        logger.info("Space in TotalCharges column has been replaced with NaN")
        # drop 11 (0.156%) rows that contains NaN values
        processed_df = processed_df.dropna()
        logger.info("NaN values in TotalCharges column ha been dropped.")
        return processed_df
    except:
        logger.error('Error: unable to clean column TotalCharges. TotalCharges is not in the input data frame.')
        raise KeyError("TotalCharges is not in the input data frame.")


def SeniorCitizen_processor(df):
    """
    helper function to clean the column SeniorCitizen_processor
    :param df: a pandas data frame contains the raw data
    :return processed_df: a pandas data frame with 'SeniorCitizen' column processed.
    """
    try:
        processed_df = df
        processed_df["SeniorCitizen"] = processed_df["SeniorCitizen"].replace({1: "Yes", 0: "No"})
        logger.info("Binary values in SeniorCitizen column have been replaced with Yes/No")
        return processed_df
    except:
        logger.error('Error: unable to clean column SeniorCitizen. SeniorCitizen is not in the input data frame.')
        raise KeyError("SeniorCitizen is not in the input data frame.")


def No_internet_service_converter(df, cols):
    """
    helper function to replace 'No internet service' to No for the following columns 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
    :param df:  a pandas data frame contains the raw data
    :param cols: a list of columns to be processed
    :return processed_df: a pandas data frame with the above six columns processed.
    """
    processed_df = df
    for i in cols:
        try:
            processed_df[i] = processed_df[i].replace({'No internet service': 'No'})
            logger.info("\"No internet service\" have been replaced with No in column %s" % i)
        except:
            logger.error('Error: unable to clean column %s.' % i + "%s is not in the input data frame." % i)
            raise KeyError("%s is not in the input data frame." % i)
    return processed_df


def drop_customerID(df):
    """
    helper function to drop the customerID column from the data frame
    :param df:  a pandas data frame contains the raw data
    :return processed_df: a pandas data frame with customerID column drop
    """
    processed_df = df
    try:
        processed_df = processed_df.drop('customerID', axis=1)
        logger.info("customerID column has been dropped")
        return processed_df
    except:
        logger.error('Error: unable to drop column customerID. customerID is not in the input data frame.')
        raise KeyError("customerID is not in the input data frame.")
