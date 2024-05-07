# Calculate correlation coefficients between Emigrants and dependent variables
correlations = {}
for var in X:
    corr_coeff, _ = pearsonr(stats[X], stats[Y])
    correlations[var] = corr_coeff

# Print summary statistics and correlations
for var in X + Y:
    print(f"Statistics for {var}:")
    print(f"Mean: {summary_stats[var]['mean']:.2f}")
    print(f"Standard Deviation: {summary_stats[var]['std']:.2f}")
    print(f"Min: {summary_stats[var]['min']:.2f}")
    print(f"Max: {summary_stats[var]['max']:.2f}")
    print(f"Correlation with {independent_var}: {correlations[var]:.2f}\n")

# Create scatter plots (optional)
for var in dependent_vars:
    plt.scatter(df[independent_var], df[var], alpha=0.5)
    plt.xlabel(independent_var)
    plt.ylabel(var)
    plt.title(f"{var} vs. {independent_var}")
    plt.show()
    
    
    # Calculate summary statistics for each variable
    summary_stats = {}
    for var in [X] + Y:
        summary = describe([var])
        summary_stats[var] = {
            'mean': summary.mean,
            'std': summary.variance**0.5,
            'min': summary.minmax[0],
            'max': summary.minmax[1]}



    stats.dropna(subset=['Emigrants', 'corruption_index', 'Temperature anomaly', 'Human Development Index'], inplace=True)

    # Define independent variable (migration) and dependent variables (corruption_index, temperature anomaly, human_development_index)
    X_migration = stats['Emigrants']
    y_corruption = stats['corruption_index']
    y_temperature = stats['Temperature anomaly']
    y_hdi = stats['Human Development Index']

    # Add constant term for intercept
    X_with_const = sm.add_constant(X_migration)

    # Fit linear regression models
    model_corruption = sm.OLS(y_corruption, X_with_const).fit()
    model_temperature = sm.OLS(y_temperature, X_with_const).fit()
    model_hdi = sm.OLS(y_hdi, X_with_const).fit()


    X = stats[['corruption_index', 'Temperature anomaly', 'Human Development Index']]
    y = stats['Emigrants']

    model = sm.OLS(y, X).fit()

    # Extract coefficients
    coefficients = model.params

    # Create a DataFrame for coefficients
    coefficients_df = pd.DataFrame({'Variable': coefficients.index, 'Coefficient': coefficients.values})

    # Save coefficients DataFrame to a Stata data file
    coefficients_df.to_stata('migan1.dta', write_index=False)

    print(model.summary())

    # Print regression summary

    print("Corruption Index:")
    print(model_corruption.summary())

    print("\nTemperature Anomaly:")
    print(model_temperature.summary())

    print("\nHuman Development Index:")
    print(model_hdi.summary())

    with open('regression_results.txt', 'w') as f:
        f.write(model.summary().as_text())
        

    # Extract coefficients and other relevant information from the regression summary
    regression_results = model.summary()

    # Save coefficients to a DataFrame
    coefficients_data = regression_results.tables[1].data
    coefficients_df = pd.DataFrame(coefficients_data, columns=coefficients_data[0])

    # Save coefficients DataFrame to a CSV file
    coefficients_df.to_csv('regression_coefficients.csv', index=False)

    coefficients_df.to_stata('stats.dta', write_index=False)

    stats= stats.drop(columns=['geometry', 'Unnamed'])
    stats= stats.drop(columns=[ 'Unnamed: 0'])


# Create the scatter plot with the regression line
plt.figure(figsize=(13, 8))
plt.scatter(X['corruption_index'], Y, alpha=0.5, label='Data points')
plt.plot(X['corruption_index'], intercept + slope * X['corruption_index'], color='red', label='Regression line')
plt.xlabel('Corruption Index')
plt.ylabel('Emigrants')
plt.title('Linear Regression: Emigrants vs. Corruption Index')
plt.legend()

# Save the plot as a PNG image
plt.savefig('scatter_plot_regression.png')

# Show the plot (optional)
plt.show()



# Select the independent and dependent variables
X = stats[['corruption_index', 'Temperature anomaly', 'Human Development Index']]
Y = stats['Emigrants']

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(X['corruption_index'], Y)

# Print regression results
print(f"Regression slope (coefficient): {slope:.4f}")
print(f"Regression intercept: {intercept:.4f}")
print(f"R-squared value: {r_value**2:.4f}")
print(f"P-value: {p_value:.4f}")



# Assume you have an 'Entity' column (replace with the actual column name)
entities = stats['Entity'].unique()

# Perform linear regression for each entity
for entity in entities:
    X = stats.loc[stats['Entity'] == entity, ['corruption_index', 'Temperature anomaly', 'Human Development Index']]
    Y = stats.loc[stats['Entity'] == entity, 'Emigrants']

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(X['corruption_index'], Y)

# Assume you have an 'Entity Volume' column (replace with the actual column name)
X1 = stats['Entity']
Y1 = stats['Emigrants']



# Print regression results
print(f"Regression slope (coefficient): {slope:.4f}")
print(f"Regression intercept: {intercept:.4f}")
print(f"R-squared value: {r_value**2:.4f}")
print(f"P-value: {p_value:.4f}")

# Create the scatter plot with the regression line
plt.figure(figsize=(13, 8))
plt.scatter(X1, Y1, alpha=0.5, label='Data points')
plt.plot(X1, intercept + slope * X1, color='red', label='Regression line')
plt.xlabel('Entity')
plt.ylabel('Emigrants')
plt.title('Linear Regression: Emigrants vs. Entity Volume')
plt.legend()

# Save the plot as a PNG image
plt.savefig('scatter_plot_entity_volume.png')

# Show the plot (optional)
plt.show()




import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Read the CSV file into a Pandas DataFrame
stats = pd.read_csv('merged_gdf.csv')

# Fill all values in the 'Year' column with 2020
stats['Year'] = 2020

# Drop rows with null values in specific columns
stats.dropna(subset=['corruption_index', 'Temperature anomaly', 'Human Development Index', 'Emigrants'], inplace=True)

stats = stats.drop(columns=['geometry', 'Unnamed: 0'])

def plot_regression(Entity, variable_name):
    X = stats[variable_name]  # Extracting independent variable
    Y = stats['Emigrants']

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(X, Y)

    # Create the scatter plot with the regression line
    plt.figure(figsize=(13, 8))
    plt.scatter(X, Y, alpha=0.5, label='Data points')
    plt.plot(X, intercept + slope * X, color='red', label='Regression line')
    plt.xlabel(variable_name)
    plt.ylabel('Emigrants')
    plt.title(f'Linear Regression: Emigrants vs. {Entity, variable_name}')
    plt.legend()

    # Save the plot as a PNG image
    plt.savefig(f'scatter_plot_{Entity, variable_name}.png')

    # Show the plot (optional)
    plt.show()

# Call the function with the desired entity and variable name
plot_regression('corruption_index')


# Assume you have an 'Entity' column (replace with the actual column name)
Entities = stats['Entity'].unique()

# Perform linear regression for each entity
for Entity in Entities:
    X1 = stats.loc[stats['Entity'] == Entity, ['corruption_index', 'Temperature anomaly', 'Human Development Index']]
    Y1 = stats.loc[stats['Entity'] == Entity, 'Emigrants']

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(X1, Y1)
    
Entity('China')









import pandas as pd
import statsmodels.api as sm

# Read the CSV file into a Pandas DataFrame (replace with the actual file path)
stats1 = pd.read_csv('merged_gdf.csv')

# Fill all values in the 'Year' column with 2020
stats1['Year'] = 2020

# Drop rows with null values in specific columns
stats1.dropna(subset=['corruption_index', 'Temperature anomaly', 'Human Development Index', 'Emigrants'], inplace=True)

# Drop unnecessary columns
stats1 = stats1.drop(columns=['geometry', 'Unnamed: 0'])

# Define independent variables (X) and dependent variable (y)
X = stats1[['corruption_index', 'Temperature anomaly', 'Human Development Index']]
y = stats1['Emigrants']

# Add a constant term to the independent variables
X = sm.add_constant(X)

# Fit the multiple linear regression model
model = sm.OLS(y, X).fit()

# Print the summary of the regression model
print(model.summary())

# Save the summary as a text file
with open('regression_summary.txt', 'w') as f:
    f.write(model.summary().as_text())

print("Summary saved as 'regression_summary.txt'")



# Save the filtered data to a new CSV file
temperature2020.to_csv("temperature2020.csv")
migration2020.to_csv("migration2020.csv")
pcorruption2020.to_csv("pcorruption2020.csv")
hdi2020.to_csv('hdi2020.csv')


stats.to_file('stats.shp')


stats.to_csv('stats.csv')

# Clean up stats DataFrame
statsmap = merged_gdf.drop(columns=['geometry'])
statsmap = statsmap.dropna(subset=['Corruption Index', 'Temperature anomaly', 'Human Development Index', 'Entity', 'Emigrants'], inplace=True)

# Export to GeoPackage
statsmap.to_file('statsmap.gpkg', driver='GPKG')

# Export to Shapefile
statsmap.to_file('statsmap.shp')



migandta = pd.read_csv('stats.csv')

migandta = migandta[['Entity','Emigrants', 'Temperature anomaly', 'Corruption Index', 'Human Development Index']]
migandta.to_stata('miganstats.dta')