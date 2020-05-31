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
        logger.info("Raw data has been loaded.")
        # 1. replace spaces with NaN in the TotalCharges column
        df['TotalCharges'] = df["TotalCharges"].replace(" ", np.nan).astype(float)
        logger.info("Space in TotalCharges column has been replaced with NaN")
        # 2.1 replace binary values to "Yes" or "No"
        df["SeniorCitizen"] = df["SeniorCitizen"].replace({1: "Yes", 0: "No"})
        logger.info("Binary values have been replaced with Yes/No")
        # 2.2 replace 'No internet service' to No for the following columns
        col_to_replace = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                        'TechSupport', 'StreamingTV', 'StreamingMovies']
        for i in col_to_replace:
            df[i] = df[i].replace({'No internet service': 'No'})
        logger.info("\"No internet service\" have been replaced with No")
        # 3. drop the id column
        df = df.drop('customerID', axis=1)
        logger.info("customerID column has been dropped")
        # export preprocessed data to a csv file
        df_to_csv(df, **config['run_preprocess_data']['save_csv'])
    except:
        logger.error("Error: unable to preprocess the raw data")