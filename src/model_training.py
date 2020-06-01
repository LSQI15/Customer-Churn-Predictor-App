import yaml
import logging
from sklearn import model_selection
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

from src.helper import csv_reader, df_to_csv


def choose_target(data, target):
    """
    helper function to select the target column for model training
    :param data: a Pandas DataFrame
    :param target: the column name of the response variable y
    :return: a pandas DataFrame containing only the response variable y
    """
    try:
        if target is None:
            logger.error("Error: target column is None.")
            return None
        else:
            if target in data.columns:
                logger.info("target column for model training has been chosen.")
                return data[target]
            else:
                logger.error("Error: target column not found in the dataset.")
                return None
    except:
        logger.error("Error: Unable to select target column for model training. Return None")
        return None


def choose_features(data, features):
    """
    helper function to select the feature column(s) for model training
    :param data: a Pandas DataFrame
    :param features: a list of column names
    :return: a pandas DataFrame containing only features X
    """
    try:
        valid_features = []
        if features is not None:
            for col in data.columns:
                if col in features:
                    valid_features.append(col)
        if valid_features is None:
            logger.error("Error: no feature is chosen. Return None")
            return None
        else:
            logger.info("Features for model training has been chosen.")
            return data[valid_features]
    except:
        logger.error("Error: Unable to select feature(s) for model training. Return None")


def train_test_split(data, target_col, feature_list, test_prop):
    """
    helper function to split the training and test set
    :param data: a Pandas DataFrame
    :param target_col: the name of response variable y
    :param feature_list: a list of column names
    :param test_prop: the percentage of data to be used for testing purpose
    :return: a list of [X_train, X_test, y_train, y_test]
    """
    try:
        # feature and target split
        features = choose_features(data, feature_list)
        target = choose_target(data, target_col)
        # train and test set split
        X_train, X_test, y_train, y_test = model_selection.train_test_split(features, target,
                                                                            test_size=test_prop,
                                                                            random_state=15)
        return [X_train, X_test, y_train, y_test]
    except:
        logger.error("Error: Unable to split train/test set for model training")


def rf_trainer(X_train, y_train, file_path, file_name):
    """
    helper function to train the random forest model and save it locally
    :param X_train: a data frame containing features in the training set
    :param y_train: a pandas series containing the response variable in the training set
    :param file_path: path to the saved model
    :param file_name: name of the saved model
    :return df: a trained random forest model
    """
    try:
        rf = RandomForestClassifier(bootstrap=True, min_samples_leaf=5, max_features='auto',
                                    random_state=115, n_jobs=4)
        rf.fit(X_train, y_train)
        logger.info("A random forest model has been trained.")
        # save the model locally
        with open(file_path + "/" + file_name, 'wb') as f:
            pickle.dump(rf, f)
        logger.info("Random forest model has been saved locally.")
        return rf
    except:
        logger.error("Error: unable to train the random forest model.")


def rf_predictor(rf, X_test, y_test):
    """
    helper function to predict the response values, using a trained random forest model
    :param rf: a trained random forest
    :param X_test: a data frame containing features in the test set
    :param y_test: a pandas series containing the response variable in the test set
    :return predictions: a pandas data frame containing the predicted probabilities, predicted responses and true
                        responses in the test set.
    """
    try:
        pred_prob = rf.predict_proba(X_test)[:, 1]
        pred_class = rf.predict(X_test)
        logger.info("Predictions have been made by the random forest Classifier.")
        # convert to a data frame
        predictions = pd.DataFrame({'pred_prob': pred_prob.round(10),
                                    'pred_class': pred_class,
                                    'y_test': y_test},
                                   columns=['pred_prob', 'pred_class', 'y_test'])
        logger.info("Predictions have been combined into a pandas data frame.")
        return predictions
    except:
        logger.error("Error: unable to predict unseen responses in the test set.")


def rf_feature_importance(rf, features):
    """
    helper function to calculate feature importance
    :param rf: a RandomForestClassifer object
    :return feat_import: data frame containing feature names and their corresponding importance
    """
    try:
        feat_import = pd.DataFrame({'feature': features, 'importance': rf.feature_importances_},
                                   columns=['feature', 'importance']).sort_values('importance', ascending=False)
        logger.info("Feature importance has been calculated.")
        return feat_import
    except:
        logger.error("Unable to calculate feature importance.")


def rf_feature_importance_plot(df, file_path, file_name):
    """
    helper function to create the feature importance plot and save it locally
    :param df: a data frame containing feature names and their corresponding importance
    :param file_path: the path to the output file
    :param file_name: the name of the output file
    """
    try:
        ax = df.plot(x='feature', y='importance', figsize=(15, 20),
                     title="Random Forest Classifier - Feature Importance", kind='barh')
        ax.invert_yaxis()
        plt.savefig(file_path + '/' + file_name, bbox_inches='tight')
        logger.info("Feature importance plot has been saved.")
    except:
        logger.error("Error: unable to plot feature importance.")


def random_forest(args):
    """
    main function to run thr random forest classifier
    :param :param args (argparse): user-input configuration file
    """
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        # read preprocessed data
        df = csv_reader(**config['run_randomForest']['read_csv'])
        logger.info("Dataset for model training has been loaded.")
        # train/test split
        X_train, X_test, y_train, y_test = train_test_split(df, **config['run_randomForest']['train_test_split'])
        df_to_csv(X_train, **config['run_randomForest']['X_train'])
        df_to_csv(X_test, **config['run_randomForest']['X_test'])
        df_to_csv(y_train.to_frame(), **config['run_randomForest']['y_train'])
        df_to_csv(y_test.to_frame(), **config['run_randomForest']['y_test'])
        logger.info("Train set and test set have been exported as .csv files")
        # Model fitting
        rf = rf_trainer(X_train, y_train, **config['run_randomForest']['rf_to_local'])
        # prediction
        predictions = rf_predictor(rf, X_test, y_test)
        df_to_csv(predictions, **config['run_randomForest']['predictions'])
        # feature importance
        feat_import = rf_feature_importance(rf, **config['run_randomForest']['calculate_importance'])
        df_to_csv(feat_import, **config['run_randomForest']['save_importance'])
        rf_feature_importance_plot(feat_import, **config['run_randomForest']['plot_importance'])
    except:
        logger.error("Error: unable to run the random forest model.")
