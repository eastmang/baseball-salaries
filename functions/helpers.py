from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import pandas as pd


# This function takes in a dataframe and a string of a column name. Then it bins the values into 3 quartiles and gets
# dummy variables for the bins so we can run trees on the data.
def cutter(frame, col):
    frame[col] = pd.qcut(frame[col], q=3, labels=[col + "_low", col + "_average", col + "_high"])
    frame = pd.concat([frame, pd.get_dummies(frame[col])], axis=1)
    frame = frame.drop([col], axis=1)
    return frame


# This function takes in an array of predictions,an array of outcomes, and a string of the model name. Then it prints
# the RMSE and R2 values for that model.
def results(test, pred, model_name):
    print("\n")
    mse = mean_squared_error(test, pred)
    rmse = np.sqrt(mse)
    print(model_name + " Root Mean Squared Error: ", rmse)

    r_squared = r2_score(test, pred)
    print(model_name + " R Squared Value: ", r_squared)
