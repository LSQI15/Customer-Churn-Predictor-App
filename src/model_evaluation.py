import logging
import yaml
import sklearn
import pickle
import pandas as pd
from sklearn import metrics

logger = logging.getLogger(__name__)

from src.helper import csv_reader, df_to_csv2


def auc_accuracy_processor(pred):
    """
    helper function to calculate the auc and accuracy of predictions
    :param pred: a pandas dataframe contains 3 columns (y_test, pred_prob and pred_class)
    """
    if 'y_test' in pred.columns and 'pred_prob' in pred.columns and 'pred_class' in pred.columns:
        y_test = pred.y_test
        pred_prob = pred.pred_prob
        pred_class = pred.pred_class
        auc = sklearn.metrics.roc_auc_score(y_test, pred_prob)
        accuracy = sklearn.metrics.accuracy_score(y_test, pred_class)
        auc_accuracy_df = pd.DataFrame(data={'auc': [auc], 'accuracy': [accuracy]})
        # output csv file
        logger.info("AUC and Accuracy have been calculated")
        return auc_accuracy_df
    else:
        logger.error("Error: unable to calculate auc/accuracy.")
        raise KeyError("One or more of the required column is not in the input data frame.")


def confusion_matrix_processor(pred):
    """
    helper function to calculate the confusion matrix
    :param pred: a pandas dataframe contains 3 columns (y_test, pred_prob and pred_class)
    """
    if 'y_test' in pred.columns and 'pred_class' in pred.columns:
        y_test = pred.y_test
        pred_class = pred.pred_class
        confusion = sklearn.metrics.confusion_matrix(y_test, pred_class)
        confusion_df = pd.DataFrame(confusion,
                                    index=['Actual negative', 'Actual positive'],
                                    columns=['Predicted negative', 'Predicted positive'])
        # output csv file
        logger.info("Confusion matrix has been calculated.")
        return confusion_df
    else:
        logger.error("Error: unable to generate confusion matrix")
        raise KeyError("One or more of the required column is not in the input data frame.")


def classification_report_processor(pred):
    """
    helper function to generate classification report
    :param pred: a pandas dataframe contains 3 columns (y_test, pred_prob and pred_class)
    """
    if 'y_test' in pred.columns and 'pred_class' in pred.columns:
        y_test = pred.y_test
        pred_class = pred.pred_class
        classification_report_dict = sklearn.metrics.classification_report(y_test, pred_class, output_dict=True)
        classification_report_df = pd.DataFrame.from_dict(classification_report_dict)
        # output csv file
        logger.info("Classification report has been calculated.")
        return classification_report_df
    else:
        logger.error("Error: unable to generate classification report")
        raise KeyError("One or more of the required column is not in the input data frame.")


def evaluate_model(args):
    """
    main function to evaluate model performance and calculate evaluation metrics
    :param
    args.config: path to configuration file
    args.in_file_path: path to the input model prediction data
    args.out_file_path: the directory of model-related output files
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    try:
        # read data
        pred = csv_reader(args.in_file_path)
        logger.info("Prediction results for model evaluation has been loaded.")
        # calculate evaluation metrics
        auc_accuracy_df = auc_accuracy_processor(pred)
        df_to_csv2(auc_accuracy_df, args.out_file_path, **config['run_model_evaluator']['auc_accuracy_processor'])
        # generate confusion matrix
        confusion_df = confusion_matrix_processor(pred)
        df_to_csv2(confusion_df, args.out_file_path, **config['run_model_evaluator']['confusion_matrix_processor'])
        # generate classification report
        classification_report_df = classification_report_processor(pred)
        df_to_csv2(classification_report_df, args.out_file_path, **config['run_model_evaluator']['classification_report_processor'])
    except:
        logger.error("Error: unable to calculate model evaluation metrics")
