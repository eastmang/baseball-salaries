import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from functions.helpers import results

# Setting global variables for this.
TESTING_SIZE = .2
RAND = 20
ESTIMATORS = 40

# Prepping the data
os.chdir('D:/personal_projects/baseball')
original = pd.read_csv('salary_data.csv')
y_values = original[['logSal']]
x_values = original.drop(['logSal', 'playerID', 'yearID'], axis=1)

# Get the training and testing sets.
x_train, x_test, y_train, y_test = train_test_split(x_values, y_values['logSal'], test_size=TESTING_SIZE,
                                                    random_state=RAND)


# Running the random forest. I optimized the learning rates and estimators instead of using a constant number.
rf = RandomForestRegressor(bootstrap=True, random_state=RAND, criterion='mse', min_samples_split=100,
                           n_estimators=ESTIMATORS)
model_rf = rf.fit(x_train, y_train)
y_pred_rf = model_rf.predict(x_test)
results(y_test, y_pred_rf, "Random Forest")

# Running the ada boosted tree. I optimized the learning rates and estimators instead of using a constant number.
boosted = AdaBoostRegressor(learning_rate=.001, n_estimators=ESTIMATORS, loss='linear', random_state=RAND)
model_ada = boosted.fit(x_train, y_train)
y_pred_ada = model_ada.predict(x_test)
results(y_test, y_pred_ada, "Ada Boosted")

# Running the gradient boosted tree. I optimized the learning rates and estimators instead of using a constant number.
gradient = GradientBoostingRegressor(loss='huber', learning_rate=.3, n_estimators=ESTIMATORS, criterion='friedman_mse',
                                     random_state=RAND)
model_grad = gradient.fit(x_train, y_train)
y_pred_grad = model_grad.predict(x_test)
results(y_test, y_pred_grad, "Gradient Boosted")

# Running the linear regression.
linear = LinearRegression()
model_linear = linear.fit(x_train, y_train)
y_pred_linear = model_linear.predict(x_test)
results(y_test, y_pred_linear, "Linear Regression")

# Predict over all the player data.
predictions = model_rf.predict(x_values)

# Finding the amount that a franchise is getting in value by taking the prediction and subtracting the actual salary
# amount.
original['predictions'] = predictions
original['profit'] = np.exp(original['predictions']) - np.exp(original['logSal'])

# Finding the 5 players that had the largest difference in the money a player brings in stats and the amount of money
# that player was paid.
top = original.nlargest(5, 'profit')

# Displaying the player, the year the difference happened, and the monetary difference.
print('\n')
print(top[['playerID', 'yearID', 'profit']].head())

# A plot of the importance of each variable in the tree.
variable_list = x_train.columns

# The plot is too crowded to look at all the variables. Instead we will plot the top 10 most important columns. First
# we need to sort the columns and then we use plotlib and seaborn to do it.
features = model_grad.feature_importances_
sorted = np.argsort(features)
weights = features[sorted][-10:]
importances = list(weights)
x_values = list(range(len(importances)))
plt.figure(figsize=(7, 6))
sns.set_context("paper", font_scale=.6, rc={"font.size":10, "axes.titlesize":16, "axes.labelsize":12})
plt.bar(x_values, importances, orientation='vertical')
plt.xticks(x_values, variable_list[sorted][-10:], rotation=75)
plt.ylabel('Importances'); plt.xlabel('Variables'); plt.title('Variable Importances')
plt.savefig("Importance Weights.jpg")
