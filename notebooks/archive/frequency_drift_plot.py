#!/usr/bin/env python3
"""
Frequency Drift Analysis - Standalone Script
Run this directly: python frequency_drift_plot.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.fft import fft, fftfreq

# Setup
plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#e0e0e0',
    'axes.labelcolor': '#ffffff',
    'axes.titlecolor': '#ffffff',
    'xtick.color': '#e0e0e0',
    'ytick.color': '#e0e0e0',
    'text.color': '#ffffff',
    'grid.color': '#3a3a5a',
    'legend.facecolor': '#16213e',
    'legend.edgecolor': '#e0e0e0',
    'legend.labelcolor': '#ffffff',
})

COLORS = {'x1': '#00d4ff', 'x2': '#ff6b35', 'forcing': '#00ff88', 'response': '#ff4488'}
DATA_DIR = Path("../data")

# Load AAM data
def load_aam_data(data_dir):
    files = sorted(data_dir.glob("ESMGFZ_AAM_v1.0_03h_*.asc.csv"))
    print(f"Found {len(files)} AAM files")
    frames = []
    for f in files:
        df = pd.read_csv(f, sep=";")
        df["datetime"] = pd.to_datetime(dict(year=df["Year"], month=df["Month"], day=df["Day"])) + pd.to_timedelta(df["Time"])
        df["X1"] = pd.to_numeric(df["Mass_X"], errors="coerce") + pd.to_numeric(df["Motion_X"], errors="coerce")
        df["X2"] = pd.to_numeric(df["Mass_Y"], errors="coerce") + pd.to_numeric(df["Motion_Y"], errors="coerce")
        frames.append(df[["datetime", "X1", "X2"]].dropna())
    return pd.concat(frames, ignore_index=True).sort_values("datetime").set_index("datetime")

print("Loading AAM data...")
aam = load_aam_data(DATA_DIR)
aam_daily = aam.resample('D').mean()
aam_daily['eq_magnitude'] = np.sqrt(aam_daily['X1']**2 + aam_daily['X2']**2)
print(f"Data: {aam_daily.index.min().date()} to {aam_daily.index.max().date()}")

# FFT function
def compute_spectrum_fft(data):
    n = len(data)
    data = data - np.mean(data)
    yf = fft(data)
    xf = fftfreq(n, 1.0)
    pos_mask = xf > 0
    period = 1.0 / xf[pos_mask]
    power = np.abs(yf[pos_mask])**2 / n
    return period, power

def find_peak_in_band(period, power, low, high):
    mask = (period >= low) & (period <= high)
    if mask.sum() > 0:
        idx = np.argmax(power[mask])
        return period[mask][idx], power[mask][idx]
    return np.nan, np.nan

# Analyze by era
windows = [
    ('1976-01-01', '1985-01-01', '1976-1985'),
    ('1985-01-01', '1995-01-01', '1985-1995'),
    ('1995-01-01', '2005-01-01', '1995-2005'),
    ('2005-01-01', '2015-01-01', '2005-2015'),
    ('2015-01-01', '2025-01-01', '2015-2025'),
]

print("\n" + "="*70)
print("PEAK FORCING FREQUENCY BY ERA")
print("="*70)
print(f"{'Era':<12} {'Annual Peak':<14} {'Power':<12} {'Chandler Peak':<14} {'Power'}")
print("-"*70)

annual_peaks = []
chandler_peaks = []

for start, end, label in windows:
    subset = aam_daily[(aam_daily.index >= start) & (aam_daily.index < end)]
    if len(subset) > 365:
        data = subset['eq_magnitude'].interpolate().dropna().values
        period, power = compute_spectrum_fft(data)
        ann_peak, ann_pow = find_peak_in_band(period, power, 300, 400)
        ch_peak, ch_pow = find_peak_in_band(period, power, 400, 500)
        annual_peaks.append((label, ann_peak))
        chandler_peaks.append((label, ch_peak))
        print(f"{label:<12} {ann_peak:>8.1f} d      {ann_pow:.2e}    {ch_peak:>8.1f} d      {ch_pow:.2e}")

# Plot frequency drift
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

years = [int(p[0][:4]) + 5 for p in annual_peaks]
ann_periods = [p[1] for p in annual_peaks]
ch_periods = [p[1] for p in chandler_peaks]

axes[0].plot(years, ann_periods, 'o-', color=COLORS['x2'], lw=3, ms=12)
axes[0].axhline(365.25, color='white', ls='--', lw=2, alpha=0.7, label='True annual (365.25d)')
axes[0].set_xlabel('Year', fontsize=12)
axes[0].set_ylabel('Peak Period (days)', fontsize=12)
axes[0].set_title('Annual Forcing Peak: Frequency Drift?', fontweight='bold', fontsize=14)
axes[0].legend(fontsize=11)
axes[0].set_ylim(300, 400)
axes[0].grid(True, alpha=0.3)

axes[1].plot(years, ch_periods, 'o-', color=COLORS['x1'], lw=3, ms=12)
axes[1].axhline(433, color='white', ls='--', lw=2, alpha=0.7, label='Chandler resonance (433d)')
axes[1].set_xlabel('Year', fontsize=12)
axes[1].set_ylabel('Peak Period (days)', fontsize=12)
axes[1].set_title('Chandler-Band Forcing Peak: Frequency Drift?', fontweight='bold', fontsize=14)
axes[1].legend(fontsize=11)
axes[1].set_ylim(400, 500)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('frequency_drift.png', dpi=150, facecolor='#1a1a2e')
print("\nSaved: frequency_drift.png")
plt.show()

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("""
- If Annual peak stays near 365d: Forcing is ON resonance
- If Chandler peak stays near 433d: Forcing is ON resonance

If BOTH are on resonance but wobble collapsed anyway,
this confirms TRANSFER FUNCTION FAILURE - Earth stopped responding
to forcing that should excite wobble.
""")
