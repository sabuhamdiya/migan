import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
import os
import difflib

# Load temperature data from CSV
temperature_df = pd.read_csv("annual-temperature-anomalies.csv")

# Filter rows where the year is 2022
filtered_df = temperature_df[temperature_df["Year"] == 2022]

# Save the filtered data to a new CSV file
filtered_df.to_csv("filtered_temperature_anomaly.csv")

# Load geo boundaries shapefile from the zip file
with ZipFile("geoBoundariesCGAZ_ADM0.zip", "r") as zip_ref:
    zip_ref.extractall("shapefiles")

# Read shapefile
shapefile_path = os.path.join("shapefiles", "geoBoundariesCGAZ_ADM0.shp")
geo_boundaries_gdf = gpd.read_file(shapefile_path)

# Merge datasets using the standardized country names
merged_gdf = geo_boundaries_gdf.merge(filtered_df, left_on='shapeName', right_on="Entity", how="left")

# Drop the column
merged_gdf.drop(columns=['shapeName'])

# Export to GeoPackage
merged_gdf.to_file('mapheatmerged.gpkg', driver='GPKG')

# Print a success message
print("Merged data saved to mapheatmerged.gpkg")
