import pytest
import pandas as pd

pd.options.mode.chained_assignment = None

from src.data_preprocess import TotalCharges_processor, SeniorCitizen_processor, No_internet_service_converter, \
    drop_customerID
from src.featurize import filter_features
from src.model_training import choose_target
from src.model_evaluation import auc_accuracy_processor, confusion_matrix_processor, classification_report_processor

"""
test drop_customerID(df) function
"""


def test_drop_customerID_valid_input():
    """
    function to test drop_customerID(df) function with valid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")

    # happy path:
    # test whether customerID is no longer a column in the data frame
    expected = preprocessed.columns
    happy_out = drop_customerID(raw).columns
    assert expected.equals(happy_out)


def test_drop_customerID_invalid_input():
    """
    function to test drop_customerID(df) function with invalid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")

    # unhappy path:
    # if customerID is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        drop_customerID(raw.drop('customerID'))


"""
Test TotalCharges_processor(df) function
"""


def test_TotalCharges_processor_valid_input():
    """
    function to test TotalCharges_processor(df) function with valid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")
    # happy path:
    # test whether the feature column generated is the same as the expected column
    expected = preprocessed['TotalCharges'].reset_index(drop=True)
    happy_out = TotalCharges_processor(raw)['TotalCharges'].reset_index(drop=True)
    assert expected.equals(happy_out)


def test_TotalCharges_processor_invalid_input():
    """
    function to test TotalCharges_processor(df) function with invalid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")

    # unhappy path:
    # if TotalCharges is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        TotalCharges_processor(raw.drop('TotalCharges'))


"""
Test SeniorCitizen_processor(df) function
"""


def test_SeniorCitizen_processor_valid_input():
    """
    function to test SeniorCitizen_processor(df) function with valid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")
    # happy path:
    # test whether the feature column generated is the same as the expected column
    expected = preprocessed['SeniorCitizen'].reset_index(drop=True)
    raw_dropna = TotalCharges_processor(
        raw)  # need to add this intermediate step as it drops na so dimension of the two data frames can match and thus can be compared
    happy_out = SeniorCitizen_processor(raw_dropna)['SeniorCitizen'].reset_index(drop=True)
    assert expected.equals(happy_out)


def test_SeniorCitizen_processor_invalid_input():
    """
    function to test SeniorCitizen_processor(df) function with invalid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")

    # unhappy path:
    # if SeniorCitizen is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        SeniorCitizen_processor(raw.drop('SeniorCitizen'))


"""
Test No_internet_service_converter(df, cols) function
"""


def test_No_internet_service_converter_valid_input():
    """
    function to test No_internet_service_converter(df, cols) function with valid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")

    # happy path:
    # test whether the feature columns generated are the same as the expected columns
    cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    expected = preprocessed[cols].reset_index(drop=True)
    raw_dropna = TotalCharges_processor(
        raw)  # need to add this intermediate step as it drops na so dimension of the two data frames can match and thus can be compared
    happy_out = No_internet_service_converter(raw_dropna, cols)[cols].reset_index(drop=True)
    assert expected.equals(happy_out)


def test_No_internet_service_converter_invalid_input():
    """
    function to test No_internet_service_converter(df, cols) function with invalid input
    """
    # load files for testing
    raw = pd.read_csv("test/unit_test_true/raw.csv")
    # invalid columns
    cols = ['NoExistingColumn', 'MSiA', 'AVC']

    # unhappy path:
    # if SeniorCitizen is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        No_internet_service_converter(raw, cols)


"""
Test choose_target(data, target) function
"""


def test_choose_target_valid_input():
    """
    function to test choose_target(data, target) function with valid input
    """
    # load files for testing
    featurized = pd.read_csv("test/unit_test_true/featurized.csv")

    # happy path:
    # test whether the target columns is the same as the expected columns
    expected = featurized['Churn']
    happy_out = choose_target(featurized, 'Churn')
    assert expected.equals(happy_out)


def test_choose_target_invalid_input():
    """
    function to test choose_target(data, target) function with invalid input
    """
    # load files for testing
    featurized = pd.read_csv("test/unit_test_true/featurized.csv")

    # unhappy path
    # if target column is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        choose_target(featurized, 'Non-Existing_Column')


"""
Test filter_features(df) function
"""


def test_filter_features_valid_input():
    """
    function to test filter_features(df) function with valid input
    """
    # load files for testing
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")

    # happy path:
    # test whether the target columns is the same as the expected columns
    expected = preprocessed.drop('Churn', axis=1)
    happy_out = filter_features(preprocessed)
    assert expected.equals(happy_out)


def test_filter_features_invalid_input():
    """
    function to test filter_features(df) function with invalid input
    """
    # load files for testing
    preprocessed = pd.read_csv("test/unit_test_true/preprocessed.csv")

    # unhappy path:
    # if target column is missing, check whether an keyError is raised.
    bad_in = preprocessed.drop('Churn', axis=1)
    with pytest.raises(KeyError):
        filter_features(bad_in)


"""
Test auc_accuracy_processor(pred) function
"""


def test_auc_accuracy_processor_valid_input():
    """
    function to test auc_accuracy_processor(pred) function with valid input
    """
    # load files for testing
    valid_in = pd.read_csv("test/unit_test_true/predictions.csv")

    # happy path:
    # test whether the function generate the same auc/accuracy output
    expected = pd.read_csv("test/unit_test_true/evaluation_auc_accuracy.csv")
    happy_out = auc_accuracy_processor(valid_in)
    assert expected.equals(happy_out)


def test_auc_accuracy_processor_invalid_input():
    """
    function to test auc_accuracy_processor(pred) function with invalid input
    """
    # load files for testing
    bad_in = pd.read_csv("test/unit_test_true/predictions.csv").drop('y_test', axis=1)

    # unhappy path:
    # if one required column is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        auc_accuracy_processor(bad_in)


"""
Test confusion_matrix_processor(pred) function
"""


def test_confusion_matrix_processor_valid_input():
    """
    function to test confusion_matrix_processor(pred) function with valid input
    """
    # load files for testing
    valid_in = pd.read_csv("test/unit_test_true/predictions.csv")

    # happy path:
    # test whether the function generate the same auc/accuracy output
    expected = pd.read_csv("test/unit_test_true/evaluation_confusion_matrix.csv")
    happy_out = confusion_matrix_processor(valid_in).reset_index(drop=True)
    assert expected.equals(happy_out)


def test_confusion_matrix_processor_invalid_input():
    """
    function to test confusion_matrix_processor(pred) function with invalid input
    """
    # load files for testing
    bad_in = pd.read_csv("test/unit_test_true/predictions.csv").drop('y_test', axis=1)

    # unhappy path:
    # if one required column is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        confusion_matrix_processor(bad_in)


"""
Test classification_report_processor(pred) function
"""


def test_classification_report_processor_valid_input():
    """
    function to test classification_report_processor(pred) function with valid input
    """
    # load files for testing
    valid_in = pd.read_csv("test/unit_test_true/predictions.csv")

    # happy path:
    # test whether the function generate the same auc/accuracy output
    expected = pd.read_csv("test/unit_test_true/evaluation_classification_report.csv").round(10)
    happy_out = classification_report_processor(valid_in).round(10).reset_index(drop=True)
    assert expected.equals(happy_out)


def test_classification_report_processor_invalid_input():
    """
    function to test classification_report_processor(pred) function with invalid input
    """
    # load files for testing
    bad_in = pd.read_csv("test/unit_test_true/predictions.csv").drop('y_test', axis=1)

    # unhappy path:
    # if one required column is missing, check whether an keyError is raised.
    with pytest.raises(KeyError):
        classification_report_processor(bad_in)