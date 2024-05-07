# Project MIGAN(Migration Information Geospatial Analysis Network)
# Aims to analyse the relation between migration as a dependent variable
# Temperature anomalies, political corruption and human development
# as independent variables for the year 2020. 

import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
import os

# Load temperature data from CSV
temperature_df = pd.read_csv("annual-temperature-anomalies.csv")
migration= pd.read_csv("migration.csv")
pcorruption=pd.read_csv('political-corruption-index.csv')
hdi=pd.read_csv('human-development-index.csv')

# Filter rows where the entity is "global" and the year is 2020
temperature2020 = temperature_df[(temperature_df["Year"] == 2020)]

# Filter migration data for the year 2020
migration2020 = migration[migration["Year"] == 2020]

# Select only the columns I need
migration2020 = migration2020[['Year','Country','Emigrants']]

# Filter Political Corruption data to 2020
pcorruption2020=pcorruption[pcorruption["Year"] == 2020]

# Filter Human Development Index
hdi2020=hdi[hdi["Year"] == 2020]

# Check for duplicate rows
migration2020_duplicate_rows = migration2020[migration2020.duplicated()]
temperature2020_duplicate_rows = temperature2020[temperature2020.duplicated()]
pcorruption2020_duplicate_rows = pcorruption2020[pcorruption2020.duplicated()]
hdi2020_duplicate_rows = hdi2020[hdi2020.duplicated()]

# Show the number of duplicate rows
num_duplicate_rows = len(migration2020_duplicate_rows)
print("Number of duplicate rows:", num_duplicate_rows)

num_duplicate_rows = len(temperature2020_duplicate_rows)
print("Number of duplicate rows:", num_duplicate_rows)

num_duplicate_rows = len(pcorruption2020_duplicate_rows)
print("Number of duplicate rows:", num_duplicate_rows)

num_duplicate_rows = len(hdi2020_duplicate_rows)
print("Number of duplicate rows:", num_duplicate_rows)

# Clean the duplicates
cleaned_migration = migration2020.drop_duplicates()

# Drop null values 
cleaned_migration = cleaned_migration.dropna()

Entities_to_delete= [' Central and Southern Asia',' Eastern and South-Eastern Asia','Australia/New Zealand',
                     'Australia and New Zealand','World','Less developed regions','Less developed regions, excluding China',
                     'Middle-income countries','Less developed regions, excluding least developed countries',
                     'Asia','Lower-middle-income countries','Upper-middle-income countries','Developed regions',
                     'Europe and Northern America','Europe','High-income countries','Least developed countries',
                     'Southern Asia','Latin America and the Caribbean','Africa','Northern Africa and Western Asia',
                     'Low-income countries','Land-locked Developing Countries (LLDC)','Eastern Europe','Western Asia',
                     'Sub-Saharan Africa','Other','Northern Africa','Eastern Africa','Small island developing States (SIDS)',
                     'Western Africa','Western Europe','Northern Europe','Central Asia','Middle Africa','Northern America',
                     'Central and Southern Asia','Eastern and South-Eastern Asia','South-Eastern Asia','South America',
                     'Central America','Eastern Asia','Southern Europe','Caribbean']

cleaned_migration = cleaned_migration[~cleaned_migration['Country'].isin(Entities_to_delete)]

cleaned_migration['Emigrants'] = cleaned_migration['Emigrants'] / 1e6

migration2020=cleaned_migration


# Load geo boundaries shapefile from the zip file
with ZipFile("world-bounds-a.zip", "r") as zip_ref:
    zip_ref.extractall("worldmap")

# Read shapefile
shapefile_path = os.path.join("worldmap", "world-bounds-a.shp")
worldmap = gpd.read_file(shapefile_path)

# Keep the countries column
worldmap = worldmap[['geometry','NA2_DESCRI']]

# Drop empty rows in the 'NA2_DESCRI' column
worldmap = worldmap.dropna(subset=['NA2_DESCRI'])

# Rename the column to 'Entity'
worldmap.rename(columns={'NA2_DESCRI': 'Entity'}, inplace=True)

# Merge GeoDataFrame with Temperature, Emigrants, Political Corruption and Human Development Index Data
merged_gdf = worldmap.merge(migration2020, left_on='Entity', right_on='Country', how='left')
merged_gdf = merged_gdf.merge(temperature2020, on='Entity', how='left')
merged_gdf = merged_gdf.merge(pcorruption2020, on='Entity', how='left')
merged_gdf = merged_gdf.merge(hdi2020, on='Entity', how='left', suffixes=('_left', '_right'))

print(merged_gdf)

# Rename columns
merged_gdf.rename(columns={'corruption_vdem_owid': 'Corruption Index','Year_y': 'Year','Temperature anomaly':'Temperature Anomaly'}, inplace=True)

# Select needed columns
merged_gdf = merged_gdf[['geometry', 'Entity', 'Year', 'Emigrants' , 'Temperature Anomaly', 'Corruption Index', 'Human Development Index']]

# Change Emigrants type to float
merged_gdf['Emigrants'] = merged_gdf['Emigrants'].astype(float)


# Check null values
print(merged_gdf.isnull().sum())

# Fill missing year rows 
merged_gdf['Year'] = 2020

# Check for null values
print(merged_gdf.isnull().sum())

# Save file as CSV
merged_gdf.to_csv('merged_gdf_full.csv')

# Save file as shapefile
merged_gdf.to_file('migan_full.shp')

# Drop null values
merged_gdf.dropna(subset=['geometry', 'Entity', 'Year', 'Emigrants' , 'Temperature Anomaly', 'Corruption Index', 'Human Development Index'], inplace=True)

# Save file as CSV
merged_gdf.to_csv('merged_gdf_clean.csv')

# Save file as shapefile
merged_gdf.to_file('migan_clean.shp')

print(merged_gdf)

# Save cleaned file as CSV
merged_gdf.to_csv('merged_gdf_clean.csv')

# Save cleaned file as shapefile
merged_gdf.to_file('migan_clean.shp')

# Define the directory name
directory = 'MIGANmap'

# Check if the directory exists
if not os.path.exists(directory):
    # If not, create it
    os.makedirs(directory)

# Save the GeoDataFrame to a shapefile in the directory
merged_gdf.to_file(os.path.join(directory, 'migan_clean.shp'))


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
stats = stats[['Entity','Year', 'Emigrants', 'Temperature Anomaly','Corruption Index','Human Development Index']]

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
plot_regression('Human Development Index')
