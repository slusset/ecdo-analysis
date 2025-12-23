#!/bin/bash

# Script to download IERS data files
# Data files are not committed to the repository

set -e

echo "Downloading IERS data files..."

# Download EOP data
echo "Downloading Earth Orientation Parameters (EOP)..."
wget -N https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt

# Download AAM data (1976 to current year)
echo "Downloading Atmospheric Angular Momentum (AAM) data..."
START_YEAR=1976
CURRENT_YEAR=$(date +%Y)

for year in $(seq $START_YEAR $CURRENT_YEAR); do
    echo "Downloading AAM data for year $year..."
    wget -N https://datacenter.iers.org/data/csv/ESMGFZ_AAM_v1.0_03h_${year}.asc.csv || echo "Warning: Failed to download data for year $year (may not exist yet)"
done

echo "Download complete!"
