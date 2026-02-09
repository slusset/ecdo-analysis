# ECDO Analysis

Statistical analysis of Earth system observables to test whether Length of Day (LOD), polar motion, and seismic activity show anomalous coupling beyond known physical processes.

## Overview

This project provides rigorous statistical analysis of:
- **Length of Day (LOD)** variations and their correlation with Atmospheric Angular Momentum (AAM)
- **Chandler wobble** characteristics extracted from polar motion data
- Future: Seismic moment release correlations

## Key Findings

### LOD-AAM Correlation Analysis

Analysis of the relationship between Earth's rotation rate (LOD) and atmospheric angular momentum:

| Metric | Value | Significance |
|--------|-------|--------------|
| Overall Pearson correlation | r = 0.48 | p < 10⁻³⁵ |
| Spearman correlation | r = 0.45 | p < 10⁻³⁰ |
| Deseasonalized correlation | r = 0.38 | p < 10⁻²¹ |
| Pre-2000 correlation | r = 0.64 | n = 288 months |
| Post-2000 correlation | r = 0.59 | n = 311 months |

**Key insight**: Strong, persistent LOD-AAM coupling confirms that atmospheric angular momentum exchange is a dominant driver of LOD variations. This must be controlled for when testing other hypotheses.

### Chandler Wobble Analysis

The Chandler wobble is a ~433-day oscillation in Earth's polar motion, distinct from the annual wobble:

| Parameter | Value |
|-----------|-------|
| Detected period | ~433 days (1.19 years) |
| Mean amplitude | ~100-150 mas |
| Polar drift rate | ~10 mas/year |

**Key observations**:
- Clear spectral separation between Chandler (~433d) and annual (~365d) wobbles
- Amplitude shows decadal variations with notable minimum around 2005-2007
- Phase evolution is generally stable with no major discontinuities

## Notebooks

### 1. LOD-AAM Correlation (`notebooks/lod_aam_correlation.ipynb`)

Analyzes the correlation between Length of Day variations and Atmospheric Angular Momentum:
- Data loading and validation (1976-present)
- Overall correlation analysis (Pearson & Spearman)
- Rolling window correlation (5, 10, 15-year windows)
- Deseasonalization to remove monthly effects
- Pre-2000 vs Post-2000 subset analysis

### 2. Chandler Wobble Analysis (`notebooks/chandler_wobble_analysis.ipynb`)

Comprehensive analysis of the Chandler wobble from IERS polar motion data:
- Spectral analysis (FFT) to identify frequency components
- Band-pass filtering to isolate Chandler (~433d) and annual (~365d) wobbles
- Removal of secular polar drift (linear detrending)
- Amplitude and phase evolution over time
- Trajectory visualization in the polar motion plane

## Data Sources

All data is obtained from the IERS (International Earth Rotation and Reference Systems Service):

| Dataset | Source | Coverage |
|---------|--------|----------|
| EOP C04 (LOD, polar motion) | [IERS Data Center](https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt) | 1962-present (daily) |
| AAM (Atmospheric Angular Momentum) | [IERS GFZ](https://datacenter.iers.org/data/csv/) | 1976-present (3-hourly) |

To download the data:
```bash
cd data
./download_data.sh
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/slusset/ecdo-analysis.git
cd ecdo-analysis

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

### Download Data

```bash
cd data
./download_data.sh
```

### Run Notebooks

```bash
# Start Jupyter
uv run jupyter notebook

# Or run a specific notebook
uv run jupyter nbconvert --to notebook --execute notebooks/chandler_wobble_analysis.ipynb
```

## Generated Figures

Figures are automatically generated when notebooks are executed. See [Figures.md](Figures.md) for all generated visualizations.

The GitHub Action automatically:
1. Runs all notebooks on push
2. Generates figures to `figures/` directory
3. Updates `Figures.md` with links to all figures
4. Commits results back to the repository

## Project Structure

```
ecdo-analysis/
├── src/ecdo_analysis/       # Python package
│   ├── __init__.py
│   └── data_loaders.py      # LOD, AAM, polar motion loaders
├── notebooks/               # Jupyter analysis notebooks
│   ├── lod_aam_correlation.ipynb
│   └── chandler_wobble_analysis.ipynb
├── data/                    # Data files (not committed)
│   ├── README.md
│   └── download_data.sh
├── figures/                 # Generated figures
├── scripts/                 # Utility scripts
│   └── generate_figures_md.py
├── .github/workflows/       # CI/CD
│   └── run-notebooks.yml
└── tests/                   # Test suite
```

---

# Scientific Methodology

## Step 0 — Declare the scientific posture (explicitly)

You are **not** trying to prove ECDO.

You are testing whether **Earth system observables show anomalous coupling inconsistent with known processes**.

Write this at the top of your notebook (seriously).

---

## Step 1 — The Null Hypothesis (H₀)

Here is a **precise, falsifiable null** you can defend:

> **H₀:**
>
> _After accounting for known atmospheric–oceanic angular momentum exchange and established oscillatory modes (seasonal cycle, ENSO-scale variability, Chandler wobble), variations in Earth rotation (LOD) and global seismic moment release are statistically independent beyond short-term stochastic correlations._

Plain English:

* LOD is driven by AAM/OAM exchange
* Seismic moment release is governed by tectonic stress accumulation
* Any apparent correlation is:
    * transient
    * non-stationary
    * explainable by known coupling
    * or an artifact of smoothing / endpoint bias

---

## Step 2 — What would reject H₀ (this matters)

You only reject the null if **all** of these are true:

1. **Persistent correlation**
    * LOD ↔ seismic moment correlation persists across decades
    * Survives rolling-window analysis

2. **Orthogonality survives**
    * Correlation remains after controlling for AAM
    * i.e., not explainable as atmosphere-driven LOD variance

3. **Low smoothing dependence**
    * Signal exists without aggressive low-pass filtering

4. **Out-of-sample robustness**
    * Relationship appears pre-2000 as well as post-2000

If any of these fail → H₀ stands.

This is a high bar by design.

---

## Step 3 — Define variables before loading data

Write this down first:

### Independent variables

* **LOD(t)** — monthly mean, ms
* **AAM(t)** — monthly mean, dimensionless or SI-normalized

### Dependent variable

* **ΣM₀(t)** — summed seismic moment per month (Nm)

### Controls

* Seasonal cycle (removed explicitly)
* ENSO proxy (optional, later)

---

## Step 4 — What you are not testing yet

Do **not** include:

* population, biosphere, finance, volcanism
* polar drift narratives
* short-window "acceleration" plots

Those are phase-2 temptations.

---

## Step 5 — The first plots (when you get there)

Only **three plots** are allowed initially:

1. Raw monthly LOD (1962–present)
2. Raw monthly seismic moment release
3. Rolling correlation (e.g., 10-year window) between them

No composites. No normalization gymnastics.

---

## Step 6 — Why this is powerful

If you **fail** to reject H₀:

* You've done real science
* You've learned where narrative amplification enters
* You can still use this knowledge for risk framing

If you **reject** H₀:

* You have something legitimately anomalous
* Stronger than any X thread
* Worth deeper investigation

Either outcome is valuable.

---

## License

See [LICENSE](LICENSE) for details.
