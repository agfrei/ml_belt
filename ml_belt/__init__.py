
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

name = 'ml_belt'

def create_dummies(df, columns, drop_first=True):
    for col in columns:
        dummy = pd.get_dummies(df[col], drop_first=drop_first)
        df = pd.concat([df, dummy], axis = 1)
    
    df.drop(columns, axis=1, inplace=True)
    return df

def encode(df, columns):
    le = LabelEncoder()
    for col in columns:
        df[col] = le.fit_transform(df[col])
    return df

def train_and_validate_model(X_train, y_train, X_test, y_test, model=None, model_class=None, model_args=None):
    if model == None:
        if model_args:
            model = model_class(**model_args)
        else:
            model = model_class()
        model.fit(X_train, y_train)
        print('Model: {0}\n\n'.format(model))
    
    y_pred = model.predict(X_test)
    
    matrix = confusion_matrix(y_test, y_pred)
    print('Confusion Matrix:\n{0}'.format(matrix))
    
    print('\n\nScore:\n{0}'.format(classification_report(y_test, y_pred)))
    
    return model