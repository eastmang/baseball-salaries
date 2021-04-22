import numpy as np
import pandas as pd
import sqlite3

def cutter(frame, col):
    frame[col] = pd.qcut(frame[col], q=3, labels=[col + "_low", col + "_average", col + "_high"])
    frame = pd.concat([frame, pd.get_dummies(frame[col])], axis=1)
    frame = frame.drop([col], axis=1)
    return frame

con = sqlite3.connect('D:/personal_projects/baseball/database/baseball.sqlite')

'''

NOTES ON WHAT I WANT FOR THE DATABASE:

TABLES:--
batting: playerID, G_batting, AB, R, H, HR, RBI, BB, SO
fielding: playerID, E, PO, A
[main key] salaries: playerID, salary, lgID, teamID, yearID
people: playerID, debut 


command to get the data
'''

command = '''SELECT salaries.playerID, salaries.salary, salaries.lgID, salaries.teamID, salaries.yearID, 
batting.playerID, batting.G, batting.AB, batting.R, batting.H, batting.HR, batting.RBI, batting.BB, batting.SO, 
batting.yearID, fielding.playerID, fielding.E, fielding.PO, fielding.A, fielding.yearID,
people.playerID, people.debut, people.bats
FROM salaries
LEFT JOIN batting ON salaries.playerID = batting.playerID AND salaries.yearID = batting.yearID 
LEFT JOIN fielding ON salaries.playerID = fielding.playerID AND fielding.yearID = salaries.yearID 
LEFT JOIN people ON salaries.playerID = people.playerID
WHERE salaries.yearID > 2000 AND batting.G > 50
GROUP BY salaries.yearID, salaries.playerID;
'''

df = pd.read_sql(command, con)

df = df.loc[:, ~df.columns.duplicated()]
continuous_vars = ['R', 'A', 'G', 'AB', 'H', 'HR', 'RBI', 'BB', 'SO', 'E', 'PO']

print(list(df))

for col_name in continuous_vars:
    df = cutter(df, col_name)

df['debutYear'] = pd.DatetimeIndex(df['debut']).year

df['rookie'] = np.where((df['yearID'] > (df['debutYear'] + 4)), 0, 1)

df = df.drop(['debutYear', 'debut'], axis=1)

df = pd.concat([df, pd.get_dummies(df['lgID'])], axis=1)
df = df.drop(['lgID'], axis=1)

df = pd.concat([df, pd.get_dummies(df['teamID'])], axis=1)
df = df.drop(['teamID'], axis=1)

df = pd.concat([df, pd.get_dummies(df['bats'])], axis=1)
df = df.drop(['bats'], axis=1)

df = df.drop(['playerID'], axis=1)

df = df.replace(np.nan, 0)

inflation_df = pd.read_csv('D:/personal_projects/baseball/inflation_data.csv', header=0)

inflation_df = inflation_df.drop(["index", "percentage"], axis=1)

inflation_df = inflation_df.rename(columns={'year': 'yearID'})

final = pd.merge(df, inflation_df, on='yearID', how='left')

final['sal_adj'] = final['salary'] * final['inflation']

final['logSal'] = np.log(final['sal_adj'])

final = final.drop(['sal_adj', 'inflation', 'salary', 'yearID'], axis=1)

final.to_csv('D:/personal_projects/baseball/salary_data.csv', index=False)
