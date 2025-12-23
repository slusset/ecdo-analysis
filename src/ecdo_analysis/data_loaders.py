"""
Data loading functions for EOP_14 (LOD) and AAM data.

Functions to load and process Earth Orientation Parameter and
Atmospheric Angular Momentum data, resampled to monthly intervals.
"""

from pathlib import Path
from typing import Optional, Union
import pandas as pd
import numpy as np


def load_lod_data(
    file_path: Union[str, Path] = "data/EOP_14_C04_IAU2000A_one_file_1962-now.txt",
    resample_freq: str = "MS"
) -> pd.DataFrame:
    """
    Load and process EOP_14 Length of Day (LOD) data.

    Parameters
    ----------
    file_path : str or Path
        Path to the EOP_14 data file
    resample_freq : str, default "MS"
        Resampling frequency (e.g., "MS" for month start, "M" for month end)

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and LOD column in milliseconds,
        resampled to specified frequency using mean aggregation
    """
    # Read the file, skipping header lines
    # The data starts after the header (around line 14)
    df = pd.read_csv(
        file_path,
        delim_whitespace=True,
        skiprows=14,
        names=[
            'Year', 'Month', 'Day', 'MJD',
            'x', 'y', 'UT1-UTC', 'LOD',
            'dX', 'dY', 'x_Err', 'y_Err',
            'UT1-UTC_Err', 'LOD_Err', 'dX_Err', 'dY_Err'
        ]
    )

    # Create datetime index
    df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df.set_index('datetime', inplace=True)

    # Convert LOD from seconds to milliseconds for better readability
    df['LOD_ms'] = df['LOD'] * 1000

    # Resample to monthly frequency (mean)
    df_monthly = df[['LOD_ms', 'LOD']].resample(resample_freq).mean()

    return df_monthly


def load_aam_data(
    data_dir: Union[str, Path] = "data",
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    resample_freq: str = "MS"
) -> pd.DataFrame:
    """
    Load and process AAM (Atmospheric Angular Momentum) data from multiple yearly files.

    Computes X3_atm as the sum of Mass_Z and Motion_Z components.

    Parameters
    ----------
    data_dir : str or Path
        Directory containing AAM CSV files
    start_year : int, optional
        Starting year to load (if None, loads all available)
    end_year : int, optional
        Ending year to load (if None, loads all available)
    resample_freq : str, default "MS"
        Resampling frequency (e.g., "MS" for month start, "M" for month end)

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and columns:
        - Mass_Z: Z-component of mass term
        - Motion_Z: Z-component of motion term
        - X3_atm: Sum of Mass_Z and Motion_Z (atmospheric excitation factor)
        Resampled to specified frequency using mean aggregation
    """
    data_path = Path(data_dir)

    # Find all AAM files
    aam_files = sorted(data_path.glob("ESMGFZ_AAM_v1.0_03h_*.asc.csv"))

    if not aam_files:
        raise FileNotFoundError(f"No AAM files found in {data_dir}")

    # Filter by year range if specified
    if start_year is not None or end_year is not None:
        filtered_files = []
        for f in aam_files:
            # Extract year from filename
            year = int(f.stem.split('_')[-1].split('.')[0])
            if start_year is not None and year < start_year:
                continue
            if end_year is not None and year > end_year:
                continue
            filtered_files.append(f)
        aam_files = filtered_files

    if not aam_files:
        raise ValueError(f"No AAM files found for year range {start_year}-{end_year}")

    # Load all files
    dfs = []
    for file_path in aam_files:
        df = pd.read_csv(file_path, sep=';')

        # Create datetime from Year, Month, Day, Time columns
        df['datetime'] = pd.to_datetime(
            df['Year'].astype(str) + '-' +
            df['Month'].astype(str).str.zfill(2) + '-' +
            df['Day'].astype(str).str.zfill(2) + ' ' +
            df['Time']
        )

        df.set_index('datetime', inplace=True)
        dfs.append(df)

    # Concatenate all years
    df_all = pd.concat(dfs, axis=0)
    df_all.sort_index(inplace=True)

    # Calculate X3_atm as sum of Mass_Z and Motion_Z
    df_all['X3_atm'] = df_all['Mass_Z'] + df_all['Motion_Z']

    # Select relevant columns and resample to monthly
    df_monthly = df_all[['Mass_Z', 'Motion_Z', 'X3_atm']].resample(resample_freq).mean()

    return df_monthly


def load_combined_data(
    lod_file: Union[str, Path] = "data/EOP_14_C04_IAU2000A_one_file_1962-now.txt",
    aam_dir: Union[str, Path] = "data",
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    resample_freq: str = "MS"
) -> pd.DataFrame:
    """
    Load both LOD and AAM data and merge them into a single DataFrame.

    Parameters
    ----------
    lod_file : str or Path
        Path to the EOP_14 data file
    aam_dir : str or Path
        Directory containing AAM CSV files
    start_year : int, optional
        Starting year to load (if None, uses overlap of both datasets)
    end_year : int, optional
        Ending year to load (if None, uses overlap of both datasets)
    resample_freq : str, default "MS"
        Resampling frequency (e.g., "MS" for month start)

    Returns
    -------
    pd.DataFrame
        Combined DataFrame with datetime index and columns from both LOD and AAM data
    """
    # Load both datasets
    df_lod = load_lod_data(lod_file, resample_freq=resample_freq)
    df_aam = load_aam_data(aam_dir, start_year, end_year, resample_freq=resample_freq)

    # Merge on datetime index (inner join to keep only overlapping dates)
    df_combined = df_lod.join(df_aam, how='inner')

    return df_combined
