import random

import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import auc, roc_curve
from sklearn.preprocessing import LabelEncoder


base_path = 'resources/{file_name}'
output_file = base_path.format(file_name='results/predictions_on_test_data.csv')
noises = ['S/N', 'Type', 'Joined Proctor on', 'Bootcamp']
non_num_cols = ['S/N', 'Joined Proctor on', 'RowNo']

def get_dataframe_for(data_class):
    file_name = 'clean/andela_{}_data.csv'.format(data_class.lower())
    print(file_name)
    file_path = base_path.format(file_name=file_name)
    category_dataframe = pd.read_csv(file_path)
    category_dataframe['Type'] = data_class
    return category_dataframe


train = get_dataframe_for('Train')
test = get_dataframe_for('Test')


fullData = pd.concat([train,test],axis=0)
num_cols = list(set(list(fullData.columns)) - set(non_num_cols))


number = LabelEncoder()
fullData["Bootcamp"] = number.fit_transform(fullData["Bootcamp"].astype('str'))

train = fullData[fullData['Type'] == 'Train']
test = fullData[fullData['Type'] == 'Test']

train['is_train'] = np.random.uniform(0, 1, len(train)) <= .75
Train, Validate = train[train['is_train'] == True], train[train['is_train'] == False]

features = list(set(list(fullData.columns)) - set(noises))


x_train = Train[list(features)].values
y_train = Train["Bootcamp"].values
x_validate = Validate[list(features)].values
y_validate = Validate["Bootcamp"].values
x_test = test[list(features)].values


random.seed(100)
rf = RandomForestClassifier(n_estimators=1000)
rf.fit(x_train, y_train)


status = rf.predict_proba(x_validate)

fpr, tpr, _ = roc_curve(y_validate, status[:,1], pos_label=1)
roc_auc = auc(fpr, tpr)

print(roc_auc)


final_status = rf.predict_proba(x_test)
test["Bootcamp"] = final_status[:,1]


test.to_csv(output_file, columns=['S/N', 'Bootcamp'])