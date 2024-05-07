# Linear Regression loop 

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


# Run Statistical Analysis
stats=pd.read_csv('merged_gdf_clean.csv')


# Drop unnecessary Columns
stats= stats.drop(columns=['geometry', 'Unnamed: 0'])

# Fill all values in the 'Year' column with 2020
stats['Year'] = 2020

# Set of variables
stats = stats[['Emigrants', 'Temperature Anomaly','Corruption Index','Human Development Index']]

stats['Temperature Anomaly'] = stats['Temperature Anomaly'].astype(float)


# loop visualizing the linear relationship between
# the specified independent variable and the number of emigrants

def plot_regression(variable_name):
    X = stats[variable_name]
    Y = stats['Emigrants']

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(X, Y)

    # Create the scatter plot with the regression line
    plt.figure(figsize=(13, 8))
    plt.scatter(X, Y, alpha=0.5, label='Data points')
    plt.plot(X, intercept + slope * X, color='red', label='Regression line')
    plt.xlabel(variable_name)
    plt.ylabel('Emigrants')
    plt.title(f'Linear Regression: Emigrants vs. {variable_name}')
    plt.legend()

    # Save the plot as a PNG image
    plt.savefig(f'scatter_plot_{variable_name}.png')

    # Show the plot
    plt.show()

# Call the function with the desired variable name
plot_regression('Temperature Anomaly')

