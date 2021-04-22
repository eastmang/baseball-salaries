import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score,mean_squared_error
testing_size = .2
rand = 8

original = pd.read_csv('D:/personal_projects/baseball/salary_data.csv')
y_values = original[['logSal']]
x_values = original.drop(['logSal'], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x_values, y_values['logSal'], test_size = testing_size, random_state = rand)

rf = RandomForestRegressor(bootstrap=True, random_state=rand, criterion='mse', min_samples_split=3,
                           n_estimators=100)
modRF = rf.fit(x_train, y_train)
y_pred = modRF.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("Root Mean Squared Error: ", rmse)

r_squared = r2_score(y_test, y_pred)
print("R Squared Value: ", r_squared)


boosted = AdaBoostRegressor(learning_rate=.008, n_estimators=100, loss='square', random_state=rand)
model_ada = boosted.fit(x_train, y_train)
y_pred = model_ada.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("Root Mean Squared Error: ", rmse)

r_squared = r2_score(y_test, y_pred)
print("R Squared Value: ", r_squared)


boosted = GradientBoostingRegressor(loss='huber', learning_rate=.007, n_estimators=650, criterion='friedman_mse')
model_boosted = boosted.fit(x_train, y_train)
y_pred = model_boosted.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("Root Mean Squared Error: ", rmse)

r_squared = r2_score(y_test, y_pred)
print("R Squared Value: ", r_squared)


linear = LinearRegression()
model_linear = linear.fit(x_train, y_train)
y_pred = model_linear.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("Root Mean Squared Error: ", rmse)

r_squared = r2_score(y_test, y_pred)
print("R Squared Value: ", r_squared)


