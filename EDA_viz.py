
'''
Exploratory Data Analysis with Visualization

'''

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV
df = pd.read_csv('dataset_part_2.csv')
print(df.head(5))

# View the relationship btw Flightnumber and PayloadMass
g = sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 2)
g.fig.suptitle("Payload Mass by Flight Number", fontsize= 20)
g.set_xticklabels(rotation=45, ha='right', fontsize=10)
x_ticks = np.arange(0, len(df['FlightNumber'].unique()), step=2)
g.set_axis_labels("Flight Number", "Payload Mass (kg)", fontsize=14)
plt.xticks(ticks=x_ticks, fontsize=10)
plt.tight_layout()
plt.show()

# View the relationship between Flight number and Launch site
plt.figure(figsize=(12, 6))
sns.countplot(y="LaunchSite", data=df, order=df['LaunchSite'].value_counts().index)
plt.title("Number of Flights by Launch Site", fontsize=20)
plt.xlabel("Number of Flights", fontsize=14)
plt.ylabel("Launch Site", fontsize=14)
plt.tight_layout()
plt.show()

# Scatterplot Flight number and Launch site
plt.figure(figsize=(12, 6))
sns.scatterplot(x="FlightNumber", y="LaunchSite", data=df, alpha=0.7)
plt.title("Number of Flights by Launch Site", fontsize=20)
plt.xlabel("Number of Flights", fontsize=14)
plt.ylabel("Launch Site", fontsize=14)
plt.tight_layout()
plt.show()




# View the relationship between Payload mass and Launch site
plt.figure(figsize=(12,6))
sns.scatterplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, palette="deep", s=100, alpha=0.7)
plt.title("Payload Mass by Launch Site", fontsize=20)
plt.xlabel("Payload Mass (kg)", fontsize=14)
plt.ylabel("Launch Site", fontsize=14)
plt.tight_layout()
plt.show()

# Visualize the relationship btw success rate and orbit type
# Group by Orbit and calculate the mean of 'Class'
success_rate = df.groupby('Orbit')['Class'].mean().reset_index()
# Rename the columns for clarity
success_rate.columns = ['Orbit', 'Success Rate']
plt.figure(figsize=(12, 6))
sns.barplot(x='Orbit', y='Success Rate', data=success_rate, hue='Orbit', legend=False)
plt.title("Success Rate by Orbit", fontsize=20)
plt.xlabel("Orbit", fontsize=14)
plt.ylabel("Success Rate", fontsize=14)
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

# FLight Number and Orbit type
plt.figure(figsize=(12, 6))
sns.scatterplot(x="FlightNumber", y="Orbit", hue="Class", data=df, palette="deep", s=100, alpha=0.7)
plt.title("Flight Number by Orbit", fontsize=20)
plt.xlabel("Flight Number", fontsize=14)
plt.ylabel("Orbit", fontsize=14)
plt.tight_layout()
plt.show()

# Relationship btw payload mass and orbit type
# FLight Number and Orbit type
plt.figure(figsize=(12, 6))
sns.scatterplot(x="PayloadMass", y="Orbit", hue="Class", data=df, palette="deep", s=100, alpha=0.7)
plt.title("Payload by Orbit", fontsize=20)
plt.xlabel("Payload", fontsize=14)
plt.ylabel("Orbit", fontsize=14)
plt.tight_layout()
plt.show()

# Visualize the launch success yearly trend (x-axis = years and y_axis average success rate)
df['year'] = df['Date'].str.split('-').str[0]

# Group by year and calculate the mean of 'Class'
success_rate = df.groupby('year')['Class'].mean().reset_index()
success_rate.columns = ['year', 'Success Rate']

# Convert year and Success Rate into lists for plotting
year = success_rate['year'].tolist() #X-axis
success_rate_values = success_rate['Success Rate'].tolist() #Y-axis

print("Year List: ", year)
print("Success Rate List: ", success_rate_values)

plt.figure(figsize=(12, 6))
plt.plot(year, success_rate_values, marker = 'o', linestyle ='-', color='b')
plt.title("Success Rate Over Years", fontsize=20)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Success Rate", fontsize=14)
plt.grid(True)
plt.show()


# Select features that will be used in success prediction
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins','Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()
print(df.columns)

# Specify the columns to be one-hot encoded
categorical_columns = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial']

# Create the one-hot encoded DataFrame
features_one_hot = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
print(features_one_hot.head())
features_one_hot.to_csv('dataset_part_3.csv', index=False)


