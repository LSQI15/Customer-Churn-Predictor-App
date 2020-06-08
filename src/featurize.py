import yaml
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

from sklearn.preprocessing import LabelEncoder
from src.helper import csv_reader, df_to_csv


def featurize(args):
    """
    main function to preprocess/clean the raw data
    :param
    args.config: path to configuration file
    args.in_file_path: path to the preprocessed data
    args.out_file_path: path to the feaurized data
    """
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        # read preprocessed data
        df = csv_reader(args.in_file_path)
        features = filter_features(df)
        logger.info("Preprocessed data has been loaded.")
        # encode binary columns (features+target)
        bi_cols = df.nunique()[df.nunique() == 2].keys().tolist()
        binary_encoder = LabelEncoder()
        for i in bi_cols:
            df[i] = binary_encoder.fit_transform(df[i])
        logger.info("Binary columns have been encoded.")
        # one-hot encode multi-category features
        cat_features = features.nunique()[features.nunique() < 5].keys().tolist()
        multi_cols = [i for i in cat_features if i not in bi_cols]
        df = pd.get_dummies(data=df, columns=multi_cols, drop_first=True)
        logger.info("Multi-category columns have been encoded.")
        # export featurized data to csv
        df_to_csv(df, args.out_file_path)
    except:
        logger.error("Error: unable to featurize the preprocessed data")


def filter_features(df):
    """
    Helper function to select only the feature columns in the dataframe
    :param df:
    :return:
    """
    if 'Churn' in df.columns:
        features = df.drop("Churn", axis=1)
        logger.info('Feature columns have been selected')
        return features
    else:
        logger.error("Target Column \'Churn\' is not in the data frame.")
        raise KeyError("Target Column \'Churn\' is not in the data frame.")