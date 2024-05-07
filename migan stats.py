# This code is used to create linear regression model

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


# Read the CSV file into a Pandas DataFrame
stats = pd.read_csv('stats.csv')

# Fill all values in the 'Year' column with 2020
stats['Year'] = 2020

# Drop rows with null values in specific columns
stats.dropna(subset=['Corruption Index', 'Temperature anomaly', 'Human Development Index', 'Entity', 'Emigrants'], inplace=True)

stats = stats.drop(columns=['Unnamed: 0'])

X = stats[['Temperature anomaly', 'Corruption Index', 'Human Development Index']]
X = sm.add_constant(X)  # Add a constant term for the intercept

# Extract the dependent variable (response)
Y = stats['Emigrants']

# Fit the linear regression model
model = sm.OLS(Y, X).fit()

# Print the regression results
print(model.summary())

# Save the regression results summary to a CSV file
with open('regression_results.csv', 'w') as f:
    f.write(model.summary().as_csv())

# Save the regression results summary to a text file
with open('regression_results.txt', 'w') as f:
    f.write(model.summary().as_text())

# Create a figure and axis
fig, ax = plt.subplots(figsize=(9, 5))

# Display the regression summary table
summary_text = model.summary().as_text()
ax.text(0.001, 0.5, summary_text, fontsize=10, family='monospace', va='center')

# Hide axes
ax.axis('off')

# Save the figure as a PNG image
plt.savefig('regression_summary.png', dpi=300, bbox_inches='tight')






