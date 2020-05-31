import logging
import pandas as pd
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
        logger.info("Load file from %s", file_loc)
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