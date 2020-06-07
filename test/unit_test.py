import pytest
import pandas as pd

pd.options.mode.chained_assignment = None

from src.data_preprocess import TotalCharges_processor, SeniorCitizen_processor, No_internet_service_converter, \
    drop_customerID
from src.model_training import choose_target

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
