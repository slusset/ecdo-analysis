# Data Files

Data files are not committed to the repository. Download the required files from the sources below.

## IERS Earth Orientation Parameters (EOP)

**Source:** IERS Data Center
**URL:** https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt
**Description:** EOP 14 C04 IAU2000A series (1962-present)

## IERS Atmospheric Angular Momentum (AAM)

**Source:** IERS Data Center - Geophysical Fluids Data
**URL:** https://www.iers.org/IERS/EN/DataProducts/GeophysicalFluidsData/geoFluids
**Description:** ESMGFZ AAM v1.0 3-hourly data (1976-present)
**Format:** Yearly CSV files

### Download Instructions

Run the download script to fetch all required data files:

```bash
cd data
./download_data.sh
```

Or manually download individual files:

```bash
cd data
# EOP data
wget https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt

# AAM data (example for specific years)
wget https://datacenter.iers.org/data/csv/ESMGFZ_AAM_v1.0_03h_2024.asc.csv
wget https://datacenter.iers.org/data/csv/ESMGFZ_AAM_v1.0_03h_2025.asc.csv
# ... repeat for other years (1976-present)
```
