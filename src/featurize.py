import yaml
import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)

from sklearn.preprocessing import LabelEncoder
from src.helper import csv_reader, df_to_csv

def feaurize(args):
    """
    main function to preprocess/clean the raw data
    :param args (argparse): user-input configuration file
    """
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        # read preprocessed data
        df = csv_reader(**config['run_featurize_data']['read_csv'])
        features = df.drop("Churn", axis=1)
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
        # export featurized file to csv
        df_to_csv(df, **config['run_featurize_data']['save_csv'])
    except:
        logger.error("Error: unable to featurize the preprocessed data")
