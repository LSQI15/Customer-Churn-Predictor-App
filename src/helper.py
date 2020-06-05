import pickle
import pandas as pd
import logging
import numpy as np
logger = logging.getLogger(__name__)


def csv_reader(file_path, file_name):
    """
    helper function to read a csv file from the given file path
    :param file_path: file path
    :param file_name: file name
    :return a pandas DataFrame
    """
    file_loc = file_path + '/' + file_name
    try:
        mydata = pd.read_csv(file_loc)
        logger.info("File %s has been loaded.", file_loc)
        return mydata
    except:
        logger.error("Error: unable to load file %s", file_loc)


def df_to_csv(df, file_path, file_name):
    """
    helper function to convert a pandas DataFrame to a csv file
    :param df: a pandas DataFrame to be exported to csv file
    :param file_path: file path
    :param file_name: file name
    """
    file_loc = file_path + '/' + file_name
    try:
        df.to_csv(file_loc, index=False)
        logger.info("%s has been saved.", file_loc)
    except:
        logger.error("Error: unable to save file %s", file_loc)


def load_model(model_path, model_name):
    """
    helper function to load the saved random forest model
    :param model_path: where the model is saved
    :param model_name: the name of the saved model
    :return rf: the saved random forest model
    """
    try:
        model_loc = model_path+'/'+model_name
        with open(model_loc, 'rb') as f:
            rf = pickle.load(f)
        logger.info('Random forest model has been loaded from %s' % model_loc)
        return rf
    except:
        logger.error('Error: unable to load the random forest model.')


def churn_predictor(rf, df):
    """
    helper function to make predictions based on user input
    :param rf: a random forest model
    :param df: a data frame that contains user input
    :return pred: a pandas data frame containing predicted probability and the predicted class
    """
    try:
        pred_prob = rf.predict_proba(df)[:, 1]
        pred_class = rf.predict(df)
        pred = pd.DataFrame({'PredProbability': pred_prob.round(10),
                             'PredClass': pred_class},
                              columns=['PredProbability', 'PredClass'])
        pred =pred.replace({'PredClass': {1: "Yes", 0: "No"}})
        logger.info("Prediction(s) have been combined into a pandas data frame.")
        return pred
    except:
        logger.error('Error: unable to make predictions for the input data frame.')

def featurize(df):
    """
    helper function to featurize user inputs for the model to make predictions; web app has measures to make sure user
    inputs are valid before he/she submit the online prediction request
    :param df: a data frame storing inputs entered by the user
    :return: a featurized dara frame for the random forest model to make predictions
    """
    try:
        # encode binary columns with 1,0
        new_df = df.replace({"Yes": 1, "No": 0, 'Male': 1, 'Female': 0})
        # one-hot encode multi-category columns (with the same encoding as the one obtained by using
        # pd.get_dummies() function in featurize.py
        new_df['MultipleLines_No phone service'] = np.where(df['MultipleLines'] == 'No phone service', 1, 0)
        new_df['MultipleLines_Yes'] = np.where(df['MultipleLines'] == 'Yes', 1, 0)
        new_df['InternetService_Fiber optic'] = np.where(df['InternetService'] == 'Fiber optic', 1, 0)
        new_df['InternetService_No'] = np.where(df['InternetService'] == 'No', 1, 0)
        new_df['Contract_One year'] = np.where(df['Contract'] == 'One year', 1, 0)
        new_df['Contract_Two year'] = np.where(df['Contract'] == 'Two year', 1, 0)
        new_df['PaymentMethod_Credit card (automatic)'] = np.where(df['PaymentMethod'] == 'Credit card (automatic)', 1, 0)
        new_df['PaymentMethod_Electronic check'] = np.where(df['PaymentMethod'] == 'Electronic check', 1, 0)
        new_df['PaymentMethod_Mailed check'] = np.where(df['PaymentMethod'] == 'Mailed check', 1, 0)
        # drop multi-category columns that have been one-hot encoded.
        new_df = new_df.drop(['MultipleLines', 'InternetService', 'Contract', 'PaymentMethod'], axis=1)
        logger.info('Preprocessed df has been featurized.')
        return new_df
    except:
        logger.error('Error: unable to featurize the preprocessed df. One or more multi-categorical variable(s) '
                     'is missing')


def make_ingest_df(rf, df):
    """
    helper function to create a data frame ready for being ingested to the database
    :param rf: a RandomForestClassifier object
    :param df: a data frame storing preprocessed data
    :return ingest_df: a data frame ready for being ingested to the database
    """
    try:
        featurized_df = featurize(df)
        pred = churn_predictor(rf, featurized_df)
        ingest_df = pd.concat([df, pred], axis=1)
        logger.info('Ingest-ready data frame has been created.')
        return ingest_df
    except:
        logger.error('Error: unable to make an ingest-ready data frame.')