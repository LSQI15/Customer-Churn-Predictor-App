import logging
import yaml
import sklearn
import pickle
import pandas as pd
from sklearn import metrics

logger = logging.getLogger(__name__)

from src.helper import csv_reader


def auc_accuracy_processor(y_test, pred_prob, pred_class, file_path, file_name):
    """
    helper function to calculate the auc and accuracy of predictions
    :param y_test: the true response class
    :param pred_prob: the predicted response probability
    :param pred_class: the predicted response class
    :param file_path: the path to the output file
    :param file_name: the name of the output file
    """
    try:
        out_file = file_path + "/" + file_name
        auc = sklearn.metrics.roc_auc_score(y_test, pred_prob)
        accuracy = sklearn.metrics.accuracy_score(y_test, pred_class)
        auc_accuracy_df = pd.DataFrame(data={'auc': [auc], 'accuracy': [accuracy]})
        # output csv file
        auc_accuracy_df.to_csv(out_file, index=False)
        logger.info("AUC and Accuracy have been calculated and exported as a .csv file")
    except:
        logger.error("Error: unable to calculate auc/accuracy.")


def confusion_matrix_processor(y_test, pred_class, file_path, file_name):
    """
    helper function to calculate the confusion matrix
    :param y_test: the true response class
    :param pred_class: the predicted response class
    :param file_path: the path to the output file
    :param file_name: the name of the output file
    """
    try:
        out_file = file_path + "/" + file_name
        confusion = sklearn.metrics.confusion_matrix(y_test, pred_class)
        confusion_df = pd.DataFrame(confusion,
                                    index=['Actual negative', 'Actual positive'],
                                    columns=['Predicted negative', 'Predicted positive'])
        # output csv file
        confusion_df.to_csv(out_file, index=False)
        logger.info("Confusion matrix has been calculated and exported as a .csv file")
    except:
        logger.error("Error: unable to generate confusion matrix")


def classification_report_processor(y_test, pred_class, file_path, file_name):
    """
    helper function to generate classification report
    :param y_test: the true response class
    :param pred_class: the predicted response class
    :param file_path: the path to the output file
    :param file_name: the name of the output file
    """
    try:
        out_file = file_path + "/" + file_name
        classification_report_dict = sklearn.metrics.classification_report(y_test, pred_class, output_dict=True)
        classification_report_df = pd.DataFrame.from_dict(classification_report_dict)
        # output csv file
        classification_report_df.to_csv(out_file, index=False)
        logger.info("Classification report has been calculated and exported as a .csv file")
    except:
        logger.error("Error: unable to generate classification report")


def evaluate_model(args):
    """
    main function to evaluate model performance and calculate evaluation metrics
    :param args (argparse): user-input configuration file
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    try:
        # read data
        pred = csv_reader(**config['run_model_evaluator']['evaluate_model'])
        logger.info("Prediction results for model evaluation has been loaded.")
        # parse the data
        y_test = pred.y_test
        pred_prob = pred.pred_prob
        pred_class = pred.pred_class
        logger.info("Prediction results for model evaluation has been parsed, and are ready for evaluation.")
        # calculate evaluation metrics
        auc_accuracy_processor(y_test, pred_prob, pred_class, **config['run_model_evaluator']['auc_accuracy_processor'])
        # generate confusion matrix
        confusion_matrix_processor(y_test, pred_class, **config['run_model_evaluator']['confusion_matrix_processor'])
        # generate classification report
        classification_report_processor(y_test, pred_class,
                                        **config['run_model_evaluator']['classification_report_processor'])
        # generate feature importance
    except:
        logger.error("Error: unable to calculate model evaluation metrics")
