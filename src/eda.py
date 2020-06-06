import yaml
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

from src.helper import csv_reader, df_to_csv


def eda(args):
    """
    main function to conduct exploratory data analysis EDA
    :param
    args.config: path to configuration file
    args.in_file_path_preprocessed: path to the input preprocessed data
    args.in_file_name_preprocessed: name of the preprocessed data
    args.in_file_path_featurized: path to the input feaurized data
    args.in_file_name_featurized: name of the input feaurized data
    args.out_file_path: path to EDA output files
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    # read featurized data
    df = csv_reader(args.in_file_path_featurized, args.in_file_name_featurized)
    # summary statistics:
    summary_maker(df, args.out_file_path, **config['run_eda']['summary_stats'])
    # correlation heatmap:
    heatmap_maker(df, args.out_file_path, **config['run_eda']['heatmap'])
    # histograms by churn/not churn
    preprocessed_df = csv_reader(args.in_file_path_preprocessed, args.in_file_name_preprocessed)
    histogram_maker(preprocessed_df, args.out_file_path, **config['run_eda']['histogram'])


def summary_maker(df, file_path, file_name):
    """
    helper method to
    :param df: a pandas data frame containing all features and the response variable
    :param file_path: file path of the output file
    :param file_name: file name of the output file
    """
    try:
        statistics = df.describe().transpose().reset_index().rename(columns={"index": "feature"})
        df_to_csv(statistics, file_path, file_name)
        logger.info('Summary statistics has been calculated and saved as a .csv file')
    except:
        logger.error("Error: unable to generate a summary statistics table")


def heatmap_maker(df, file_path, file_name):
    """
    Helper method to generate a heatmap and save it locally
    :param df: a pandas data frame containing all features and the response variables
    :param file_path: file path of the output file
    :param file_name: file name of the output file
    """
    try:
        corr = df.corr()
        ax = plt.subplots(figsize=(15, 15))
        ax = sns.heatmap(
            corr,
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            horizontalalignment='right'
        )
        plt.savefig(file_path + '/' + file_name)
        logger.info('Correlation Heatmap has been generated and saved as a .png image')
    except:
        logger.error("Error: unable to create a heatmap.")


def histogram_maker(df, file_path, target_col):
    """
    helper function to create a histogram and save it locally
    :param df: a pandas data frame containing all features and the response variables
    :param file_path: file path of the output files
    :param target_col: the name of the target column
    """
    try:
        target = df[target_col]
        features = df.drop(target_col, axis=1)
        for feat in features.columns:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.hist([
                features[target == "Yes"][feat].values,
                features[target == "No"][feat].values],
                label=["Yes", "No"])
            ax.legend(loc='upper right', title="Churn")
            plt.title("Customer Churn by %s" % (feat))
            ax.set_xlabel(' '.join(feat.split('_')).capitalize())
            ax.set_ylabel('Number of observations')
            fig.savefig(file_path + '/{}_histogram.png'.format(feat))
            logger.info("Histogram for {} has been created and exported as a .png image".format(feat))
        logger.info("All histograms have been created.")
    except:
        logger.error("Error: unable to create histogram(s).")
