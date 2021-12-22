"""
Author : Shivam Ojha
Version : 1
Version Date : 10th Dec 2021
Description : Python function to predict crash severity and 
analyze crash data. Set TRAIN_MODEL flag to True to train models.
"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Set this to True if you want to train the models again as part of the airflow pipeline
# SVM takes considerable time to train
TRAIN_MODEL = False


def get_df_from_db(database_url, sql_statement):
    """
    Function to get dataframe from a table

    Args:
        database_url ([string]): [Database URL]

    Returns:
        df_ (dataframe): dataframe returned from the sql query
    """
    df_ = pd.read_sql_query(sql_statement, database_url)
    return df_


def transform_time(x):
    """
    Function to map hour value to datetime

    Args:
        x (datetime): datetime object

    Returns:
        (str): daytime
    """
    if (x.hour > 4) and (x.hour <= 8):
        return 'Early Morning'
    elif (x.hour > 8) and (x.hour <= 12):
        return 'Morning'
    elif (x.hour > 12) and (x.hour <= 16):
        return'Noon'
    elif (x.hour > 16) and (x.hour <= 20) :
        return 'Evening'
    elif (x.hour > 20):
        return'Night'
    elif (x.hour <= 4):
        return'Late Night'


def severity_calculate(x):
    """
    Function to map severity value

    Args:
        x (int): number of people

    Returns:
        (str): hazard level
    """
    if (x > 3):
        return 'Very High'
    elif (x > 2):
        return 'High'
    elif (x > 1):
        return 'Medium'
    else:
        return 'Low'


def calculate_corr_matrix(corr_df, corr_col):
    """
    Method to calculate correlation matrix

    Args:
        corr_df (dataframe): dataframe
        corr_col (list): list of columns in dataframe
    """
    le1 = LabelEncoder()
    encoded_corr_df = corr_df[corr_df.columns[:]].apply(le1.fit_transform)
    encoded_corr_df.corr()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    cax = ax.matshow(encoded_corr_df.corr(), interpolation='nearest')
    fig.colorbar(cax)

    xaxis = np.arange(len(corr_col))
    ax.set_xticks(xaxis)
    ax.set_yticks(xaxis)
    ax.set_xticklabels(corr_col, rotation=45)
    ax.set_yticklabels(corr_col)

    plt.savefig('Correlation matrix', dpi=300)
    plt.show()


def generate_roc_curve(y_test, pred_prob_lr):
    # multi-class classification LR
    # roc curve for classes
    fpr = {}
    tpr = {}
    thresh ={}
    n_class = 4
    for i in range(n_class):
        fpr[i], tpr[i], thresh[i] = roc_curve(y_test, pred_prob_lr[:,i], pos_label=i)
    # Plotting
    plt.figure(figsize=(15, 12))
    plt.plot(fpr[0], tpr[0], linestyle='--',color='orange', label='Class 0: Low')
    plt.plot(fpr[1], tpr[1], linestyle='--',color='green', label='Class 1: Medium')
    plt.plot(fpr[2], tpr[2], linestyle='--',color='blue', label='Class 2: High')
    plt.plot(fpr[3], tpr[3], linestyle='--',color='red', label='Class 3: Very High')
    plt.title('Multiclass ROC curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive rate')
    plt.legend(loc='best')
    plt.savefig('Multiclass LR ROC',dpi=300)

def main():
    """
    Main function
    """
    database_url = os.getenv('database_url')
    sql_statement = '''select * from {}.{}'''.format('merged_data', 'merged_data_table')
    final_df = get_df_from_db(database_url, sql_statement)
    final_df.reset_index(inplace=True)
    del final_df['index']
    final_df['crash_time'] = pd.to_datetime(final_df['crash_time'])
    final_df['day_time'] = final_df['crash_time'].apply(transform_time)
    final_df = final_df.dropna(axis=0, subset=['zip_code', 'location_latitude', 'location_longitude'])

    final_df['crash_date'] = pd.to_datetime(final_df['crash_date'])
    final_df['crash_month'] = final_df['crash_date'].dt.month
    final_df['crash_day'] = final_df['crash_date'].dt.day

    final_df['helper1'] =   final_df['number_of_persons_killed']*3 + final_df['number_of_persons_injured']*1

    final_df['hazard_level'] = final_df['helper1'].apply(severity_calculate)
    del final_df['crash_time']
    del final_df['crash_date']
    del final_df['helper1']

    # Create corr_df, used for correlation matrix
    corr_df = final_df
    corr_col = ['zip_code', 'location_latitude', 'location_longitude',
       'number_of_persons_injured', 'number_of_persons_killed', 'Temp',
       'Condition', 'Precip Rate', 'Dew', 'Wind Speed', 'day_time',
       'crash_month', 'crash_day', 'hazard_level']
    print("Correlation Matrix computed.")
    calculate_corr_matrix(corr_df, corr_col)

    if TRAIN_MODEL:

        le_ = LabelEncoder()
        encoded_df = final_df[final_df.columns[:]].apply(le_.fit_transform)

        # Prepare training and test sets
        X = np.array(encoded_df[['zip_code', 'day_time', 'Temp', 'Condition', 'Dew', 'Wind Speed', 'Precip Rate',
                            'number_of_persons_injured', 'number_of_persons_killed']])
        y = np.array(encoded_df['hazard_level'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)


        # Logistic Regression
        clf_lr = LogisticRegression(random_state=0, max_iter=45).fit(X_train, y_train)

        y_pred_lr = clf_lr.predict(X_test)
        pred_prob_lr = clf_lr.predict_proba(X_test)
        lr_acc = accuracy_score(y_test, y_pred_lr)
        print("Logistic Regression Accuracy: ", lr_acc)
        generate_roc_curve(y_test, pred_prob_lr)

        # Gradient Boost Classifier
        clf_gbc = GradientBoostingClassifier(n_estimators=19, learning_rate=0.03,
                                 max_depth=1, random_state=0).fit(X_train, y_train)
        y_pred_gbc = clf_gbc.predict(X_test)
        gbc_acc = accuracy_score(y_test, y_pred_gbc)
        pred_prob_gbc = clf_gbc.predict_proba(X_test)
        print("Gradient Boosting Classifier: ", gbc_acc)

        # SVM
        clf_svm = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        clf_svm.fit(X_train, y_train)
        y_pred_svm = clf_svm.predict(X_test)
        svm_acc = accuracy_score(y_test, y_pred_svm)
        print("SVM Accuracy: ", svm_acc)

if __name__ == '__main__':
    main()
