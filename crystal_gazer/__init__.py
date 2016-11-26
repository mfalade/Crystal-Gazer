import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_curve, auc

train = pd.read_csv('../resources/andela_training_data.csv')
test = pd.read_csv('../resources/andela_test_data.csv')

train['Type'] = 'Train'
test['Type'] = 'Test'

fullData = pd.concat([train,test],axis=0)

print(fullData.columns)
print(fullData.describe())

ID_col = ['S/N']
target_col = ["Stage"]
row_col = ["RowNo"]
date_col = ["Joined Proctor on"]
num_cols = list(set(list(fullData.columns))-set(row_col)-set(ID_col)-set(target_col)-set(date_col))
other_col = ['Type']

number = LabelEncoder()
fullData["Stage"] = number.fit_transform(fullData["Stage"].astype('str'))

train = fullData[fullData['Type'] == 'Train']
test = fullData[fullData['Type'] == 'Test']

train['is_train'] = np.random.uniform(0, 1, len(train)) <= .75
Train, Validate = train[train['is_train'] == True], train[train['is_train'] == False]

features = list(set(list(fullData.columns))-set(ID_col)-set(target_col)-set(other_col)-set(date_col))

x_train = Train[list(features)].values
y_train = Train["Stage"].values
x_validate = Validate[list(features)].values
y_validate = Validate["Stage"].values
x_test = test[list(features)].values

random.seed(100)
rf = RandomForestClassifier(n_estimators=1000)
rf.fit(x_train, y_train)

status = rf.predict_proba(x_validate)
print(status)

fpr, tpr, _ = roc_curve(y_validate, status[:,1], pos_label=1)
roc_auc = auc(fpr, tpr)

print(roc_auc)

final_status = rf.predict_proba(x_test)
test["Stage"] = final_status[:,1]
test.to_csv('model_output.csv', columns=['S/N','Stage','Bootcamp'])
