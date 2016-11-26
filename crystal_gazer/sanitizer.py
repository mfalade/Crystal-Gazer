from datetime import datetime
from random import choice

import pandas as pd


DIRTY_DATA_FILE = 'resources/dirty/hackathon_data.csv'


def convert_percentage_string_to_float(some_str):
    """Convert given string input to float.

    Arguments:
      some_str: (str) A string of the format '80.00%'
    Returns:
      result: (float) A float of the format 0.88
    """
    return float(some_str.replace('%', '')) / 100


def cleanup_data(dataframe):
    df_cols = dataframe.columns.values

    if '% Score' in df_cols:
      dataframe['% Score'] = dataframe['% Score'].apply(convert_percentage_string_to_float)

    if 'Bootcamp' in df_cols:
      dataframe['Bootcamp'] = dataframe['Bootcamp'].apply(int)
    else:
      dataframe['Bootcamp'] = 0

    return dataframe
    



if __name__ == '__main__':
  now = datetime.now().microsecond
  dataframe = pd.read_csv(DIRTY_DATA_FILE)

  dataframe = cleanup_data(dataframe)

  split_point = int(len(dataframe) * 0.7)

  training_data = dataframe[:split_point]
  test_data = dataframe[split_point:]

  dataframe.to_csv('resources/clean/hackathon_full_data_{now}.csv'.format(now=now))
  test_data.to_csv('resources/clean/hackathon_test_data_{now}.csv'.format(now=now))
  training_data.to_csv('resources/clean/hackathon_train_data_{now}.csv'.format(now=now))

  print("DATA HAS BEEN CLEANED UP FOR >>>> {now}.".format(now=now))
  print('Check your resources/clean dir to view em.')
