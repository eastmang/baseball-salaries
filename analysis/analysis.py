import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from functions.helpers import results

TESTING_SIZE = .2
RAND = 8

original = pd.read_csv('D:/personal_projects/baseball/salary_data.csv')
y_values = original[['logSal']]
x_values = original.drop(['logSal'], axis=1)

# Get the training and testing sets.
x_train, x_test, y_train, y_test = train_test_split(x_values, y_values['logSal'], test_size=TESTING_SIZE,
                                                    random_state=RAND)

# Running the random forest. I optimized the learning rates and estimators instead of using a constant number.
rf = RandomForestRegressor(bootstrap=True, random_state=RAND, criterion='mse', min_samples_split=50,
                           n_estimators=100)
modRF = rf.fit(x_train, y_train)
y_pred_rf = modRF.predict(x_test)
results(y_test, y_pred_rf, "Random Forest")

# Running the ada boosted tree. I optimized the learning rates and estimators instead of using a constant number.
boosted = AdaBoostRegressor(learning_rate=.007, n_estimators=100, loss='square', random_state=RAND)
model_ada = boosted.fit(x_train, y_train)
y_pred_ada = model_ada.predict(x_test)
results(y_test, y_pred_ada, "Ada Boosted")

# Running the gradient boosted tree. I optimized the learning rates and estimators instead of using a constant number.
gradient = GradientBoostingRegressor(loss='huber', learning_rate=.2, n_estimators=100, criterion='friedman_mse',
                                     random_state=RAND)
model_grad = gradient.fit(x_train, y_train)
y_pred_grad = model_grad.predict(x_test)
results(y_test, y_pred_grad, "Gradient Boosted")

# Running the linear regression.
linear = LinearRegression()
model_linear = linear.fit(x_train, y_train)
y_pred_linear = model_linear.predict(x_test)
results(y_test, y_pred_linear, "Linear Regression")
