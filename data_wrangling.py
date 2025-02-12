
'''
Objective: Perform exploratory data analysis to find patterns in the data and determine training labels.

Booster landing outcomes will be converted into training labels; 1 = booster landed successfully, 
and 2 = booster landing was unsuccessful.
True Ocean (mission outcome was successful), or False Ocean (mission outcome was not successful),
True RTLS or False RTLS , True ASDs or False ASDS
'''

# Import libraries
import pandas as pd
import numpy as np

# load the data
df = pd.read_csv('dataset_part_1.csv')

# Calculate the percentage of the missing values in each attribute
print(df.isnull().sum()/len(df)*100)

print(df.dtypes)

# Calculate number of launches on each site (check column LaunchSite)'
launch_counts = df['LaunchSite'].value_counts()
print(launch_counts)

# Count the number and occurence of each orbit
orbit_counts = df['Orbit'].value_counts()
print(orbit_counts)

# Count the number of occurence of mission outcome of the orbits
landing_outcomes = df['Outcome'].value_counts()
for i, outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
    
bad_outcomes = set(landing_outcomes.keys()[[1,3,5,6,7]])
print(bad_outcomes)

# Create a landing_class list
landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]
print(landing_class)
num_failures = landing_class.count(0)
print("Number of failures: {}".format(num_failures))

# The landing_class variable will represent the classification variable.
df['Class'] = landing_class
df[['Class']].head(8)
df.head(5)

# Count the number of complete failures to land
complete_failures = df['Class'].value_counts()[0]
print(complete_failures)

# Success rate
print(df['Class'].mean())

# Export it to a new csv file
df.to_csv('dataset_part_2.csv', index=False)