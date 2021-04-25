import numpy as np
import pandas as pd
import sqlite3
from functions.helpers import cutter


con = sqlite3.connect('D:/personal_projects/baseball/database/baseball.sqlite')

'''
NOTES ON WHAT I WANT FOR THE DATABASE:

TABLES:--
salaries: playerID, salary, lgID, teamID, yearID
pitching: playerID [[REMOVE PITCHERS]]  
batting: playerID, G_batting, AB, R, H, HR, RBI, BB, SO
fielding: playerID, E, PO, A
people: playerID, debut 
'''

# Creates a table with the desired columns. It also only keeps years after 1996 (the year the researcher was born). I
# decided this was a good arbitrary cutoff because it is most interesting to me. It also only keeps players that have
# more than 50 games. I did this because it means that the players that are included should be almost entirely starting
# players and not  just substitutes for a minor injury.
command = '''SELECT salaries.playerID, salaries.salary, salaries.lgID, salaries.teamID, salaries.yearID, 
batting.playerID, batting.G, batting.AB, batting.R, batting.H, batting.HR, batting.RBI, batting.BB, batting.SO, 
batting.yearID, fielding.playerID, fielding.E, fielding.PO, fielding.A, fielding.yearID, Pitching.playerID,
people.playerID, people.debut, people.bats
FROM salaries
LEFT JOIN Pitching USING (playerID)
LEFT JOIN batting USING (playerID, yearID)
LEFT JOIN fielding USING (playerID, yearID)
LEFT JOIN people USING (playerID)
WHERE salaries.yearID > 1995 AND batting.G > 50 AND Pitching.playerID IS NULL
GROUP BY salaries.yearID, salaries.playerID;
'''

# Executing the SQL command
df = pd.read_sql(command, con)

# Removing duplicates from the joins
df = df.loc[:, ~df.columns.duplicated()]

# A list of all of the continuous variables.
continuous_vars = ['R', 'A', 'G', 'AB', 'H', 'HR', 'RBI', 'BB', 'SO', 'E', 'PO']

# Going through all of the continuous columns and making dummy variables for them to run the trees on.
for col_name in continuous_vars:
    df = cutter(df, col_name)

# Extracting just the year from the date variable.
df['debutYear'] = pd.DatetimeIndex(df['debut']).year

# This gives a 1 for anyone playing within the first 4 years of their time in the MLB (to label rookies).
df['rookie'] = np.where((df['yearID'] > (df['debutYear'] + 4)), 0, 1)

# Getting rid of the now extraneous columns
df = df.drop(['debutYear', 'debut'], axis=1)

# This next part gets dummy variables for the teams and leagues and removes the old columns.
df = pd.concat([df, pd.get_dummies(df['lgID'])], axis=1)
df = df.drop(['lgID'], axis=1)

df = pd.concat([df, pd.get_dummies(df['teamID'])], axis=1)
df = df.drop(['teamID'], axis=1)

df = pd.concat([df, pd.get_dummies(df['bats'])], axis=1)
df = df.drop(['bats'], axis=1)

# The encoding from the original database for some variables just uses a NAN value for a 0 value. I do not know why.
df = df.replace(np.nan, 0)

# Reading in a csv of inflation data taken from the federal reserve.
inflation_df = pd.read_csv('D:/personal_projects/baseball/inflation_data.csv', header=0)

# Removing the two extra columns
inflation_df = inflation_df.drop(["index", "percentage"], axis=1)

# Renaming the year so that I can join.
inflation_df = inflation_df.rename(columns={'year': 'yearID'})

# Left joining the baseball and inflation data in pandas.
final = pd.merge(df, inflation_df, on='yearID', how='left')

# Getting the inflation adjusted salaries
final['sal_adj'] = final['salary'] * final['inflation']

# Getting the log of the salaries since salary data is notoriously skewed.
final['logSal'] = np.log(final['sal_adj'])

# Removing the now superfluous columns
final = final.drop(['sal_adj', 'inflation', 'salary'], axis=1)

# Saving the data.
final.to_csv('D:/personal_projects/baseball/salary_data.csv', index=False)
