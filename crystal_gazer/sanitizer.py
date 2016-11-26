from random import choice

import pandas as pd


DIRTY_DATA_FILE = 'resources/dirty/hackathon_data.csv'
UNIQUE_STAGES = [
     'Bootcamp Week 1',
     'Application Review',
     'Admissions Committee',
     'Offer',
     'Pre- Fellowship',
     'Plum.io',
     'Cut from Bootcamp Week 1',
     'Unqualified Candidates',
     'Boot Camp Week 2',
     'Andela Proctor',
     'Dropped out of Bootcamp',
     'Face to Face'
]

def get_dataframe(file_path):
  return pd.read_csv('resources/dirty/hackathon_data.csv')

def convert_percentage_string_to_float(some_str):
    """The name says it all.

    Arguments:
      some_str: (str) A string of the format '80.00%'
    Returns:
      result: (float) A float of the format 0.88
    """
    return float(string.replace('%', '')) / 100


def sanitize_data():
  dirty_data_df = get_dataframe(DIRTY_DATA_FILE)
  dirty_data_df['Stage'] = dirty_data_df['Stage'].replace('n/a', random.choice(UNIQUE_STAGES))
  dirty_data_df['% Score'] = dirty_data_df['% Score'].apply(convert_percentage_string_to_float)

  training_data = dirty_data_df[: 440]
  test_data = dirty_data_df[440:]

  dirty_data_df.to_csv('resources/clean/hackathon_data.csv')
  test_data.to_csv('resources/clean/andela_test_data.csv')
  training_data.to_csv('resources/clean/andela_train_data.csv')

  print("DATA HAS BEEN CLEANED UP.")
  print('Check your resources/clean dir to view em.')
