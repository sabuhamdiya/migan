import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
import os

# Load temperature data from CSV
temperature_df = pd.read_csv("annual-temperature-anomalies.csv")
migration= pd.read_csv("migration.csv")

# Filter rows where the entity is "global" and the year is 2018
filtered_df = temperature_df[(temperature_df["Year"] == 2018)]

# Filter migration data for the year 2018
migration2018 = migration[migration["Year"] == 2018]

# Save the filtered data to a new CSV file
filtered_df.to_csv("filtered_temperature_anomaly.csv")

# Load geo boundaries shapefile from the zip file
with ZipFile("geoBoundariesCGAZ_ADM0.zip", "r") as zip_ref:
    zip_ref.extractall("shapefiles")

# Read shapefile
shapefile_path = os.path.join("shapefiles", "geoBoundariesCGAZ_ADM0.shp")
geo_boundaries_gdf = gpd.read_file(shapefile_path)

# Merge GeoDataFrame with temperature anomaly data
merged_gdf = geo_boundaries_gdf.merge(filtered_df, left_on='shapeName', right_on="Entity", how="right")
merged_gdf = merged_gdf.drop(columns='shapeName')
merged_gdf = merged_gdf.merge(migration2018, left_on='Country', right_on='Entity', how='left')


# Export to GeoPackage
merged_gdf.to_file('mapheat1.gpkg', driver='GPKG')

# Print a success message
print("Merged data saved to mapheat.gpkg")


  