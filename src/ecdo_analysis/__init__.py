"""
ECDO Analysis Package

Statistical analysis of Earth system observables:
- Length of Day (LOD) variations
- Atmospheric Angular Momentum (AAM)
- Seismic moment release

This package provides utilities for testing the null hypothesis that
LOD and seismic moment release are statistically independent beyond
short-term stochastic correlations.
"""

__version__ = "0.1.0"

from .data_loaders import load_lod_data, load_aam_data, load_combined_data

__all__ = [
    "load_lod_data",
    "load_aam_data",
    "load_combined_data",
]
